"""Stage 7: Ingest if needed, hybrid contextual retrieve if neeed, web search if needed, generate, return answer"""

import logging
from typing import Callable

from langchain.retrievers import EnsembleRetriever
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.messages import SystemMessage, ToolMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_tavily import TavilySearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import ToolNode

from src.main.util.llm_factory import get_chat_model, get_embedding_model

TOOL_NODE = "tools"

# INGESTION ############################################################################################################


_logger = logging.getLogger(__name__)
_vector_store_dir = "./data/vector_stores/book_6"


def _has_documents():
    embedding_model = get_embedding_model()
    vector_store = Chroma(persist_directory=_vector_store_dir, embedding_function=embedding_model)
    return len(vector_store.get().get("documents", [])) > 0


def _get_chunks() -> list[Document]:
    documents = TextLoader("./data/raw/book/frank_hardys_choice.txt").load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    raw_chunks = text_splitter.split_documents(documents)

    with open("./data/raw/book/frank_hardys_choice.txt") as f:
        stuff = f.read()

    contextualizer_prompt = ChatPromptTemplate.from_messages([
        ("human", """\
<document> 
{stuff} 
</document> 
Here is the chunk we want to situate within the whole document 
<chunk> 
{chunk} 
</chunk> 
Please give a short succinct context to situate this chunk within the overall document for the purposes of \
improving search retrieval of the chunk. Answer only with the succinct context and nothing else."""),
    ])

    contextualizer_chain = contextualizer_prompt | get_chat_model() | StrOutputParser()
    contextualized_chunks = [
        Document(
            page_content=f"""
<chunk>
<context>
{contextualizer_chain.invoke({"chunk": chunk.page_content, "stuff": stuff})}
</context>
<content>
{chunk.page_content}
</content>
</chunk>
""",
            metadata=chunk.metadata,
        )
        for chunk in raw_chunks
    ]

    return contextualized_chunks


def _ingest_documents():
    _logger.info("Ingesting documents...")
    embedding_model = get_embedding_model()
    Chroma.from_documents(documents=(_get_chunks()), embedding=embedding_model, persist_directory=_vector_store_dir)
    _logger.info("Documents ingested and vector store saved.")


# TOOLS ################################################################################################################

def hybrid_contextual_retrieve(query: str) -> str:
    """
    This is a hybrid vector store and BM25 retriever tool that can be used to retrieve the most accurate information about the book Frank Hardy's Choice.

    Args:
        query: The query related to the book Frank Hardy's Choice.

    Returns:
        The retrieved chunks as a single string.
    """
    _has_documents() or _ingest_documents()

    embedding_model = get_embedding_model()
    vector_store = Chroma(persist_directory=_vector_store_dir, embedding_function=embedding_model)
    vector_retriever = vector_store.as_retriever()

    bm25_retriever = BM25Retriever.from_texts(vector_store.get().get("documents", []))

    hybrid_retriever = EnsembleRetriever(retrievers=[vector_retriever, bm25_retriever], weights=[0.5, 0.5])

    docs = hybrid_retriever.invoke(query)
    chunks = [doc.page_content for doc in docs]
    return "\n\n".join(chunks)


tavily = TavilySearch(
    max_results=5,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # include_domains=None,
    # exclude_domains=None
)

tools = [tavily, hybrid_contextual_retrieve]

# GRAPH ################################################################################################################

SYSTEM_PROMPT = """\
You are a helpful assistant.
You always prefix every response with "ARPA: ".
When you use information obtained from the web, you always reference the URL at the end of your response. 
"""  # TODO

model = get_chat_model().bind_tools(tools)


def node_llm(state: MessagesState) -> MessagesState:
    response = model.invoke([SystemMessage(SYSTEM_PROMPT)] + state["messages"])
    return {"messages": [response]}


def edge_agent_choice(state: MessagesState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        if len(last_message.tool_calls) > 1:
            raise ValueError("Only one tool call is allowed at a time.")
        return last_message.tool_calls[0]["name"]
    else:
        return END


def create_tool_call_node(tool_function: Callable) -> Callable[[MessagesState], MessagesState]:
    def node(state: MessagesState) -> MessagesState:
        tool_call = state["messages"][-1].tool_calls[0]
        result = tool_function(**tool_call["args"])
        tool_message = ToolMessage(content=str(result), tool_call_id=tool_call["id"])
        return {"messages": [tool_message]}

    return node


def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return TOOL_NODE
    return END


def create_graph() -> CompiledGraph:
    graph = StateGraph(MessagesState)

    graph.add_node(node_llm.__name__, node_llm)
    graph.add_node(TOOL_NODE, ToolNode(tools))

    graph.add_edge(START, node_llm.__name__)
    graph.add_conditional_edges(node_llm.__name__, should_continue, [TOOL_NODE, END])
    graph.add_edge(TOOL_NODE, node_llm.__name__)

    return graph.compile(checkpointer=MemorySaver())


def create_chain() -> Runnable:
    return create_graph()

from typing import Callable

from langchain_core.messages import SystemMessage, ToolMessage
from langchain_core.runnables import Runnable
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import ToolNode

from src.main.util.llm_factory import get_chat_model

TOOL_NODE = "tools"

# TOOLS ################################################################################################################

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

# TODO: HybridRetriever

tools = [tavily]

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

"""Stage 5: Ingest if needed, retrieve, generate, return answer and context"""

import logging

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableParallel, RunnablePassthrough, RunnablePick
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.main.util.llm_factory import get_chat_model, get_embedding_model

_logger = logging.getLogger(__name__)
_vector_store_dir = "./data/vector_stores/arxiv_1"

urls = [
    # https://arxiv.org/list/cs.AI/recent as of 2024-11-13
    "https://arxiv.org/html/2411.08028v1",
    "https://arxiv.org/html/2411.08024v1",
    "https://arxiv.org/html/2411.08003v1",
    "https://arxiv.org/html/2411.07983v1",
    "https://arxiv.org/html/2411.07955v1",
    "https://arxiv.org/html/2411.07942v1",
    "https://arxiv.org/html/2411.07940v1",
    "https://arxiv.org/html/2411.07871v1",
    "https://arxiv.org/html/2411.07841v1",
    "https://arxiv.org/html/2411.07814v1",
]


def _has_documents():
    embedding_model = get_embedding_model()
    vector_store = Chroma(persist_directory=_vector_store_dir, embedding_function=embedding_model)
    return len(vector_store.get().get("documents", [])) > 0


def _get_chunks() -> list[Document]:
    documents = WebBaseLoader(web_paths=urls).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(documents)


def _ingest_documents():
    _logger.info("Ingesting documents...")
    embedding_model = get_embedding_model()
    Chroma.from_documents(documents=_get_chunks(), embedding=embedding_model, persist_directory=_vector_store_dir)
    _logger.info("Documents ingested and vector store saved.")


def create_chain() -> Runnable:
    _has_documents() or _ingest_documents()
    _logger.info("Creating chain...")
    chat_model = get_chat_model()
    embedding_model = get_embedding_model()
    vector_store = Chroma(persist_directory=_vector_store_dir, embedding_function=embedding_model)
    retriever = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_messages([
        ("human", """\
    You are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, just say that you don't know.
    Use three sentences maximum and keep the answer concise.
    Question: {question} 
    Context: {formatted_context} 
    Answer:"""),
    ])

    def join(strings: list[str]):
        return "\n\n".join(strings)

    def extract_chunks(docs: list[Document]):
        return [doc.page_content for doc in docs]

    return ({
                "question": RunnablePassthrough(),
                "retrieved_context": retriever | extract_chunks,
            }
            | RunnableParallel({
                "question": RunnablePick("question"),
                "retrieved_context": RunnablePick("retrieved_context"),
                "formatted_context": RunnablePick("retrieved_context") | join,
            })
            | RunnableParallel({
                "answer": prompt | chat_model | StrOutputParser(),
                "retrieved_context": RunnablePick("retrieved_context"),
            }))


def run():
    _logger.info("Running app...")
    rag_chain = create_chain()
    while True:
        question = input("Your question (or 'q' to quit): ")
        if question.strip() == "q":
            print("Bye!")
            break
        else:
            response = rag_chain.invoke(question)
            print(f"Assistant: {response['answer']}")


if __name__ == "__main__":
    load_dotenv()
    run()
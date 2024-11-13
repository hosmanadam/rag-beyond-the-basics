"""Stage 4: Ingest if needed, retrieve, generate, return answer"""

import logging

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.main.util.llm_factory import get_chat_model, get_embedding_model

_logger = logging.getLogger(__name__)
_vector_store_dir = "./data/vector_stores/book_3"


def _has_documents():
    embedding_model = get_embedding_model()
    vector_store = Chroma(persist_directory=_vector_store_dir, embedding_function=embedding_model)
    return len(vector_store.get().get("documents", [])) > 0


def _get_chunks() -> list[Document]:
    documents = TextLoader("./data/raw/book/frank_hardys_choice.txt").load()
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
    Context: {context}
    Answer:"""),
    ])

    def format_chunks(docs: list[Document]):
        return "\n\n".join(doc.page_content for doc in docs)

    return ({"context": retriever | format_chunks, "question": RunnablePassthrough()}
            | prompt
            | chat_model
            | StrOutputParser())


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
            print(f"Assistant: {response}")


if __name__ == "__main__":
    load_dotenv()
    run()

"""Stage 3: Ingest, retrieve, generate, return answer - but something is wrong"""

import logging

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.main.util import chat_cli
from src.main.util.llm_factory import get_chat_model, get_embedding_model

_logger = logging.getLogger(__name__)


def create_chain() -> Runnable:
    _logger.info("Creating chain...")
    _logger.warning("This version always re-ingests the book into the vector store.")
    chat_model = get_chat_model()
    embedding_model = get_embedding_model()

    documents = TextLoader("./data/raw/book/frank_hardys_choice.txt").load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    chunks = text_splitter.split_documents(documents)
    vector_store = Chroma.from_documents(documents=chunks, embedding=embedding_model)
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

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

    return ({
                "context": retriever | format_chunks,
                "question": RunnablePassthrough()
            }
            | prompt
            | chat_model
            | {"answer": StrOutputParser()})


if __name__ == "__main__":
    load_dotenv()
    chat_cli.run(chain=create_chain())

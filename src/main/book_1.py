"""Stage 2: Stuff, generate, return answer"""

import logging

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough

from src.main.util.llm_factory import get_chat_model

_logger = logging.getLogger(__name__)


def create_chain() -> Runnable:
    _logger.info("Creating chain...")
    chat_model = get_chat_model()

    with open("./data/raw/book/frank_hardys_choice.txt") as f:
        stuff = f.read()

    prompt = ChatPromptTemplate.from_messages([
        ("human", f"""\
    You are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, just say that you don't know.
    Use three sentences maximum and keep the answer concise.
    Context: {stuff}
    Question: {{question}}
    Answer:"""),
    ])

    return ({"question": RunnablePassthrough()}
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
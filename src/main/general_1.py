"""Stage 1"""

import logging

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

from src.main.util.llm_factory import get_chat_model

_logger = logging.getLogger(__name__)


def create_chain() -> Runnable:
    return get_chat_model() | StrOutputParser()


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

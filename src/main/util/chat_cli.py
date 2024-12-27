import logging

from langchain_core.runnables import Runnable

_logger = logging.getLogger(__name__)


def run(chain: Runnable):
    _logger.info("Running app...")
    while True:
        question = input("Your question (or 'q' to quit): ")
        if question.strip() == "q":
            print("Bye!")
            break
        else:
            response = chain.invoke(question)
            print(f"Assistant: {response['answer']}")

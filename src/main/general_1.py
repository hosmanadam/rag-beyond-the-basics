"""Stage 1"""

import logging

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

from src.main.util import chat_cli
from src.main.util.llm_factory import get_chat_model

_logger = logging.getLogger(__name__)


def create_chain() -> Runnable:
    return get_chat_model() | {"answer": StrOutputParser()}


if __name__ == "__main__":
    load_dotenv()
    chat_cli.run(chain=create_chain())

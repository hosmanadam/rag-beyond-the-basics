import logging

import chainlit as cl

from src.main.util import rag_loader

_logger = logging.getLogger(__name__)


@cl.on_message
async def main(message: cl.Message):
    chain = rag_loader.get("book_1")  # TODO: Select
    response = chain.invoke(message.content)
    await cl.Message(response["answer"]).send()

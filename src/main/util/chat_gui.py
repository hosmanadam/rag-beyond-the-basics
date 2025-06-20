import logging

import chainlit as cl
from chainlit.input_widget import Select

from src.main.rag import general_1
from src.main.util import rag_loader
from src.main.util.responses import get_response

_logger = logging.getLogger(__name__)

setting_rag_module_name = "rag_module_name"
rag_module_name = general_1.__name__.split(".")[-1]
rag_chain = rag_loader.load_chain(rag_module_name)


@cl.on_message
async def on_message(message: cl.Message):
    _logger.info(f"Message from user: {message.content}")
    response = get_response(message.content, rag_chain)
    await cl.Message(response).send()


@cl.on_chat_start
async def start():
    await cl.ChatSettings(
        [
            Select(
                id=setting_rag_module_name,
                label="RAG Module",
                values=rag_loader.get_names(),
                initial_value=rag_module_name,
            ),
        ]
    ).send()
    await cl.Message(
        content=f"Starting chat over RAG module `{rag_module_name}`.\n"
                f"You can switch modules in the chat settings below."
    ).send()


@cl.on_settings_update
async def on_settings_update(settings: dict):
    _logger.info(f"Updated settings: {settings}")
    global rag_module_name
    selected_rag_module_name = settings.get(setting_rag_module_name)
    if selected_rag_module_name != rag_module_name:
        rag_module_name = selected_rag_module_name
        global rag_chain
        rag_chain = rag_loader.load_chain(selected_rag_module_name)
        await cl.Message(f"Switched to RAG module `{rag_module_name}`").send()

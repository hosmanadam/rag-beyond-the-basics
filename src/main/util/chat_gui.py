import logging

import chainlit as cl
from chainlit.input_widget import Select
from langchain_core.messages import HumanMessage

from src.main.rag import general_1
from src.main.util import rag_loader

_logger = logging.getLogger(__name__)

setting_rag_module_name = "rag_module_name"
rag_module_name = general_1.__name__.split(".")[-1]
rag_chain = rag_loader.load_chain(rag_module_name)


@cl.on_message
async def on_message(message: cl.Message):
    _logger.info(f"Message from user: {message.content}")
    try:
        # Assume simple chain
        response = rag_chain.invoke(message.content)["answer"]
    except ValueError:
        # Turns out it's a graph, needs to be called differently # HACK
        end_state = rag_chain.invoke(
            input={"messages": [HumanMessage(message.content)]},
            config={"configurable": {"thread_id": cl.context.session.id}}
        )
        response = end_state["messages"][-1].content
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

from typing import Callable

from langchain_core.messages import SystemMessage, ToolMessage
from langchain_core.runnables import Runnable
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph
from langgraph.graph.graph import CompiledGraph

from src.main.util.llm_factory import get_chat_model

# TOOLS ################################################################################################################

# TODO


# GRAPH ################################################################################################################

SYSTEM_PROMPT = """\
You are a helpful assistant. You always prefix every response with "ARPA: "
"""  # TODO

tools = []  # TODO
model = get_chat_model()


def node_llm(state: MessagesState) -> MessagesState:
    response = model.invoke([SystemMessage(SYSTEM_PROMPT)] + state["messages"])
    return {"messages": [response]}


def edge_agent_choice(state: MessagesState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        if len(last_message.tool_calls) > 1:
            raise ValueError("Only one tool call is allowed at a time.")
        return last_message.tool_calls[0]["name"]
    else:
        return END


def create_tool_call_node(tool_function: Callable) -> Callable[[MessagesState], MessagesState]:
    def node(state: MessagesState) -> MessagesState:
        tool_call = state["messages"][-1].tool_calls[0]
        result = tool_function(**tool_call["args"])
        tool_message = ToolMessage(content=str(result), tool_call_id=tool_call["id"])
        return {"messages": [tool_message]}

    return node


def create_graph() -> CompiledGraph:
    graph = StateGraph(MessagesState)

    graph.add_node(node_llm.__name__, node_llm)
    for tool in tools:
        graph.add_node(tool.__name__, create_tool_call_node(tool))

    graph.add_edge(START, node_llm.__name__)
    graph.add_conditional_edges(node_llm.__name__, edge_agent_choice)
    for tool in tools:
        graph.add_edge(tool.__name__, node_llm.__name__)

    return graph.compile(checkpointer=MemorySaver())


def create_chain() -> Runnable:
    return create_graph()

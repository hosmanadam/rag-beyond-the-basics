from langchain_core.messages import HumanMessage
from langchain_core.runnables import Runnable, RunnableSequence
from langgraph.graph.state import CompiledStateGraph


def get_response(question: str, runnable: Runnable) -> str:
    if isinstance(runnable, RunnableSequence):
        return runnable.invoke(question)["answer"]
    elif isinstance(runnable, CompiledStateGraph):
        end_state = runnable.invoke(
            input={"messages": [HumanMessage(question)]},
            config={"configurable": {"thread_id": "please_dont_deploy_me_to_prod"}}
        )
        return end_state["messages"][-1].content
    else:
        raise TypeError(f"Can't get response from {runnable.__class__.__name__}")

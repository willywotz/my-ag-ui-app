from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import call_model

def build_graph(checkpointer):
    builder = StateGraph(AgentState)
    builder.add_node("agent", call_model)
    builder.set_entry_point("agent")
    builder.add_edge("agent", END)
    return builder.compile(checkpointer=checkpointer)
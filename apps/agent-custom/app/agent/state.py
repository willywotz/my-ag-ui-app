from typing import Annotated
from langgraph.graph import MessagesState
from copilotkit.langgraph import CopilotKitState

class AgentState(MessagesState, CopilotKitState):
    pass
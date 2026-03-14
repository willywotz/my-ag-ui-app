import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from .state import AgentState

# llm = ChatOpenAI(model="gpt-4o", streaming=True)

llm = ChatOpenAI(
    model="/model",
    base_url="http://thaillm.or.th/api/typhoon/v1",
    api_key="dummy",
    default_headers={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "apikey": os.getenv("THAILLM_API_KEY"),
    },
    # max_tokens=2048,
    temperature=0,
)

async def call_model(state: AgentState) -> dict:
    response = await llm.ainvoke(state["messages"])
    return {"messages": [response]}
"""
This is the main entry point for the agent.
It defines the workflow graph, state, tools, nodes and edges.
"""

import os

from copilotkit import CopilotKitMiddleware
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from src.query import query_data
from src.todos import AgentState, todo_tools

THAILLM_API_KEY = os.getenv("THAILLM_API_KEY")
if not THAILLM_API_KEY:
    raise ValueError("THAILLM_API_KEY is not set in the environment variables.")

agent = create_agent(
    model=ChatOpenAI(
        model="/model",
        base_url="http://thaillm.or.th/api/typhoon/v1",
        api_key="dummy",
        default_headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "apikey": THAILLM_API_KEY,
        },
        max_tokens=2048,
        temperature=0,
    ),
    tools=[query_data, *todo_tools],
    middleware=[CopilotKitMiddleware()],
    state_schema=AgentState,
    system_prompt="""
        You are a helpful assistant that helps users understand CopilotKit and LangGraph used together.

        Be brief in your explanations of CopilotKit and LangGraph, 1 to 2 sentences.

        When demonstrating charts, always call the query_data tool to fetch all data from the database first.
    """,
)

graph = agent

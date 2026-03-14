import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

import os
from dotenv import load_dotenv

load_dotenv()
os.environ["LANGGRAPH_FASTAPI"] = "true"

import uvicorn
from fastapi import FastAPI
from copilotkit import LangGraphAGUIAgent
from ag_ui_langgraph import add_langgraph_fastapi_endpoint

from contextlib import asynccontextmanager
# from copilotkit.integrations.fastapi import add_fastapi_endpoint
# from copilotkit import CopilotKitSDK, LangGraphAgent
from app.checkpointer import get_checkpointer
from app.agent.graph import build_graph

class _GraphProxy:
    _graph = None
    def __getattr__(self, name):
        return getattr(self._graph, name)

graph_proxy = _GraphProxy()

@asynccontextmanager
async def lifespan(app: FastAPI):
    checkpointer = await get_checkpointer()
    graph_proxy._graph = build_graph(checkpointer)
    yield

app = FastAPI(lifespan=lifespan)

add_langgraph_fastapi_endpoint(
    app=app,
    agent=LangGraphAGUIAgent(
        name="sample_agent",
        description="An example agent to use as a starting point for your own agent.",
        graph=graph_proxy,
    ),
    path="/",
)

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}

def main():
    port = int(os.getenv("PORT", "8123"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    main()

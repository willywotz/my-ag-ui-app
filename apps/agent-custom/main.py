import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
os.environ["LANGGRAPH_FASTAPI"] = "true"

app = FastAPI()

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}

def main():
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    main()

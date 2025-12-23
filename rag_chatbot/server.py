from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent import run_agent_query
import uvicorn
import asyncio   


# uv run uvicorn server:app --host 127.0.0.1 --port 8001


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    try:
        agent_response = await run_agent_query(request.query)
        return QueryResponse(response=agent_response)

    except asyncio.TimeoutError:
        return QueryResponse(
            response="AI is slow right now. Please try again."
        )

    except Exception as e:
        return QueryResponse(
            response=f"Server error: {str(e)}"
        )

@app.get("/")
def read_root():
    return {"message": "RAG Chatbot server is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

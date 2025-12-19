from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent_query
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from openai import APITimeoutError

#  uv run uvicorn server:app --host 127.0.0.1 --port 8001

app = FastAPI()

# Add CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
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

    except APITimeoutError:
        return QueryResponse(
            response="AI is slow right now. Please try again in a moment."
        )


@app.get("/")
def read_root():
    return {"message": "RAG Chatbot server is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

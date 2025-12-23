import os
import cohere
from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient

# Load environment variables
load_dotenv()

# Env variables
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "humanoid_ai_book"

# Initialize Cohere async client
cohere_client = cohere.AsyncClient(COHERE_API_KEY)

# Initialize Qdrant async client
qdrant = AsyncQdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

# -----------------------------
# Get embedding from Cohere
# -----------------------------
async def get_embedding(text: str) -> list[float]:
    response = await cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",
        texts=[text],
    )
    return response.embeddings[0]

# -----------------------------
# Retrieve relevant chunks (FIXED)
# -----------------------------
async def retrieve(query: str) -> list[dict]:
    embedding = await get_embedding(query)

    result = await qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=embedding,
        limit=5,
        score_threshold=0.1,
    )

    # ✅ Normalize result → always a list of points
    if isinstance(result, tuple):
        points = result[0]
    else:
        points = result

    documents = []

    for point in points:
        payload = getattr(point, "payload", None)
        if payload and "text" in payload:
            documents.append({"text": payload["text"]})

    return documents




# -----------------------------
# Main RAG Agent
# -----------------------------
async def run_agent_query(query: str) -> str:
    # 1. Retrieve documents
    documents = await retrieve(query)

    # 2. Ask Cohere chat model
    response = await cohere_client.chat(
        model="command-r-plus", 
        message=query,
        documents=documents,
        temperature=0.3,
    )

    return response.text

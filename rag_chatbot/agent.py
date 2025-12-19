from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import set_tracing_disabled, function_tool
import os
from dotenv import load_dotenv

load_dotenv()
set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
cohere_api_key = os.getenv("COHERE_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    timeout=60,        # wait longer
    max_retries=2      # retry automatically
)


model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=provider
)

import cohere
from qdrant_client import QdrantClient

# Initialize Cohere client
cohere_client = cohere.Client(cohere_api_key)
# Connect to Qdrant
qdrant = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key,
)

def get_embedding(text):
    """Get embedding vector from Cohere Embed v3"""
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",
        texts=[text],
    )
    return response.embeddings[0]

@function_tool
def retrieve(query: str) -> list[str]:
    """
    Retrieve ONLY relevant chunks from the book.
    If nothing relevant is found, return empty list.
    """
    embedding = get_embedding(query)

    result = qdrant.search(
        collection_name="humanoid_ai_book",
        query_vector=embedding,
        limit=5,
        score_threshold=0.25  # 🔒 strict book-only filter
    )

    if not result:
        return []

    return [point.payload["text"] for point in result]


async def run_agent_query(query: str) -> str:
    """
    Runs the RAG agent with the given query and returns the final response.
    """
    agent = Agent(
        name="Assistant",
        instructions="""
You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
To answer the user question, first call the tool `retrieve` with the user query.
Use ONLY the returned content from `retrieve` to answer.
If the answer is not in the retrieved content, say "I don't know".
""",
        model=model,
        tools=[retrieve]
    )

    result = await Runner.run(
        agent,
        input=query,
    )

    return result.final_output
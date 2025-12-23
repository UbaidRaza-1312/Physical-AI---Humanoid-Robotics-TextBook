import os
import requests
import xml.etree.ElementTree as ET
import trafilatura
import cohere
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# -------------------------------------
# CONFIG
# -------------------------------------
SITEMAP_URL = "https://physical-ai-humanoid-robotics-text.vercel.app/sitemap.xml"
COLLECTION_NAME = "humanoid_ai_book"
EMBED_MODEL = "embed-english-v3.0"
VECTOR_SIZE = 1024  # Cohere v3 embedding dimension

# -------------------------------------
# Load ENV
# -------------------------------------
load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# -------------------------------------
# Clients
# -------------------------------------
cohere_client = cohere.Client(COHERE_API_KEY)

qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

# -------------------------------------
# Step 1 — Extract URLs from sitemap
# -------------------------------------
def get_all_urls(sitemap_url: str) -> list[str]:
    response = requests.get(sitemap_url, timeout=15)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    urls = []

    for child in root:
        loc = child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc is not None and loc.text:
            urls.append(loc.text)

    print(f"\nFound {len(urls)} URLs")
    return urls

# -------------------------------------
# Step 2 — Download page + extract text
# -------------------------------------
def extract_text_from_url(url: str) -> str | None:
    try:
        html = requests.get(url, timeout=15).text
        text = trafilatura.extract(html)
        return text
    except Exception as e:
        print("[ERROR] Failed to extract:", url, e)
        return None

# -------------------------------------
# Step 3 — Chunk text (with overlap)
# -------------------------------------
def chunk_text(text: str, max_chars=1200, overlap=200) -> list[str]:
    chunks = []
    while len(text) > max_chars:
        split_pos = text[:max_chars].rfind(". ")
        if split_pos == -1:
            split_pos = max_chars
        chunks.append(text[:split_pos])
        text = text[split_pos - overlap :]
    chunks.append(text)
    return chunks

# -------------------------------------
# Step 4 — Create embedding
# -------------------------------------
def embed(text: str) -> list[float]:
    response = cohere_client.embed(
        model=EMBED_MODEL,
        input_type="search_document",
        texts=[text],
    )
    return response.embeddings[0]

# -------------------------------------
# Step 5 — Create Qdrant collection (safe)
# -------------------------------------
def create_collection():
    if qdrant.collection_exists(COLLECTION_NAME):
        print("Qdrant collection already exists. Skipping creation.")
        return

    print("Creating Qdrant collection...")
    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE,
        ),
    )

# -------------------------------------
# Step 6 — Save chunk to Qdrant
# -------------------------------------
def save_chunk(chunk: str, chunk_id: int, url: str):
    vector = embed(chunk)

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=chunk_id,
                vector=vector,
                payload={
                    "text": chunk,     # 🔥 used by agent.py
                    "url": url,
                    "chunk_id": chunk_id,
                },
            )
        ],
    )

# -------------------------------------
# MAIN INGESTION PIPELINE
# -------------------------------------
def ingest_book():
    urls = get_all_urls(SITEMAP_URL)
    create_collection()

    global_id = 1

    for url in urls:
        print("\nProcessing:", url)
        text = extract_text_from_url(url)

        if not text:
            print("No text found, skipping.")
            continue

        chunks = chunk_text(text)

        for chunk in chunks:
            save_chunk(chunk, global_id, url)
            print(f"Saved chunk {global_id}")
            global_id += 1

    print("\n✅ Ingestion completed!")
    print("Total chunks stored:", global_id - 1)

# -------------------------------------
# RUN
# -------------------------------------
if __name__ == "__main__":
    ingest_book()

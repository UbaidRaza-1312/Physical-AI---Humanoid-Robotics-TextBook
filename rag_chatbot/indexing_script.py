import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Qdrant

# Load .env
load_dotenv()

# Qdrant config
QDRANT_URL = "https://173afb85-1ba2-4c8e-98d2-e0da69faa82d.us-east4-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")  # Better to use env variable
QDRANT_COLLECTION_NAME = "humanoid_ai_book"

# Google GenAI config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

EMBEDDING_MODEL = "text-embedding-004"

def load_documents(directory_path: str):
    loader = DirectoryLoader(
        directory_path,
        glob="**/*.md*",
        loader_cls=UnstructuredMarkdownLoader,
        recursive=True,
        show_progress=True
    )
    return loader.load()

def chunk_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return text_splitter.split_documents(documents)

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GEMINI_API_KEY
    )

def store_in_qdrant(chunks, embeddings):
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    # Recreate collection if exists
    vector_size = len(embeddings.embed_query("test"))
    client.recreate_collection(
        collection_name=QDRANT_COLLECTION_NAME,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE)
    )

    # Create Qdrant vectorstore
    vectorstore = Qdrant.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=QDRANT_COLLECTION_NAME,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )
    return vectorstore

if __name__ == "__main__":
    docs_directory = "./docs"
    documents = load_documents(docs_directory)
    chunks = chunk_documents(documents)
    embeddings = get_embeddings()
    vectorstore = store_in_qdrant(chunks, embeddings)
    print("Indexing complete!")

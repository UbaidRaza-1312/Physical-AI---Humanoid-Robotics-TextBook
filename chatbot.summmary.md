RAG Chatbot Build Summary
This document provides a complete summary of the code and configuration required to build and run the RAG (Retrieval-Augmented Generation) chatbot.

first of all initialize your uv venv by using this command
uv venv

then activate it

1. Backend Server (main.py)
This FastAPI script runs the backend server. It provides a /chat endpoint for the RAG pipeline and a /qdrant-status endpoint to check the database status.

import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from qdrant_client import QdrantClient, models
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv() # Load environment variables from .env file

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Qdrant configuration
QDRANT_URL = "QDRANT_URL"
QDRANT_API_KEY = "you qdrant_api_key"
QDRANT_COLLECTION_NAME = "docusaurus_book_rag"

# Google GenAI configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

EMBEDDING_MODEL = "text-embedding-004"
GENERATION_MODEL = "gemini-2.5-flash"

# Initialize Qdrant Client
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

# Initialize Embedding Model
embeddings_model = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=GEMINI_API_KEY
)

# Initialize LLM for generation
llm = ChatGoogleGenerativeAI(
    model=GENERATION_MODEL,
    google_api_key=GEMINI_API_KEY
)

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # 1. Generate embedding for the user query
        query_embedding = embeddings_model.embed_query(request.query)

        # 2. Retrieve relevant chunks from Qdrant
        search_result = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_embedding,
            limit=3 # top_k=3 as per requirements
        )
        
        context_texts = [hit.payload["text"] for hit in search_result]
        
        # 3. Prepare prompt for LLM
        prompt_template = """
        You are a helpful assistant for a Docusaurus book. Answer the user's question based on the provided context only.
        If the answer is not in the context, politely state that you don't have enough information.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        # 4. Generate response using LLM
        full_context = "\n\n".join(context_texts)
        
        formatted_prompt = prompt.format(context=full_context, question=request.query)
        response = llm.invoke(formatted_prompt)

        return {"response": response.content}

    except Exception as e:
        logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f'An error occurred: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/qdrant-status")
async def get_qdrant_status():
    try:
        collection_info = qdrant_client.get_collection(QDRANT_COLLECTION_NAME)
        return {
            "collection_name": QDRANT_COLLECTION_NAME,
            "status": "active",
            "point_count": collection_info.points_count
        }
    except Exception as e:
        # Log the exception for debugging
        logging.error(f"Error checking Qdrant status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error checking Qdrant status: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
2. Python Dependencies (requirements.txt)
These are the required Python libraries. Pinning qdrant-client to version 1.7.3 is critical to avoid errors.

qdrant-client==1.7.3
langchain
langchain-community
langchain-google-genai
langchain-text-splitters
fastapi
uvicorn
python-dotenv
chardet
3. Frontend Chat Widget (ChatWidget.js)
This React component creates the chat UI. The fetch URL has been updated to use an environment variable for easy deployment, falling back to localhost for local development.

import React, { useState, useEffect, useRef } from 'react';
import styles from './ChatWidget.module.css';

const ChatWidget = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [message, setMessage] = useState('');
    const [conversation, setConversation] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const chatWindowRef = useRef(null);

    const toggleChat = () => {
        setIsOpen(!isOpen);
    };

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!message.trim()) return;

        const userMessage = { text: message, sender: 'user' };
        setConversation((prev) => [...prev, userMessage]);
        setMessage('');
        setIsLoading(true);

        try {
            // Use environment variable for API URL, fallback to localhost
            const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/chat';
            
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: message }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            setConversation((prev) => [...prev, { text: data.response, sender: 'bot' }]);
        } catch (error) {
            console.error('Error sending message:', error);
            setConversation((prev) => [...prev, { text: `Error: ${error.message}`, sender: 'bot' }]);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (chatWindowRef.current) {
            chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
        }
    }, [conversation]);

    return (
        <>
            {isOpen && (
                <div className={styles.chatWindow}>
                    <div className={styles.chatHeader} onClick={toggleChat}>
                        AI Assistant
                        <button className={styles.closeButton}>×</button>
                    </div>
                    <div className={styles.chatBody} ref={chatWindowRef}>
                        {conversation.length === 0 && !isLoading && (
                            <div className={styles.welcomeMessage}>
                                Hi there! How can I help you with the Docusaurus book?
                            </div>
                        )}
                        {conversation.map((msg, index) => (
                            <div key={index} className={`${styles.message} ${styles[msg.sender]}`}>
                                {msg.text}
                            </div>
                        ))}
                        {isLoading && (
                            <div className={`${styles.message} ${styles.bot}`}>
                                <div className={styles.loadingDots}>
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        )}
                    </div>
                    <form className={styles.chatInputForm} onSubmit={sendMessage}>
                        <input
                            type="text"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            placeholder="Type your message..."
                            disabled={isLoading}
                        />
                        <button type="submit" disabled={isLoading} aria-label="Send message">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M3.478 2.405a.75.75 0 0 0-.926.94l2.432 7.905H13.5a.75.75 0 0 1 0 1.5H4.984l-2.432 7.905a.75.75 0 0 0 .926.94 60.519 60.519 0 0 0 18.445-8.986.75.75 0 0 0 0-1.218A60.517 60.517 0 0 0 3.478 2.405Z"/></svg>
                        </button>
                    </form>
                </div>
            )}
            {!isOpen && (
                <button className={styles.chatToggleButton} onClick={toggleChat} aria-label="Open chat">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28" fill="currentColor">
                        <path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/>
                    </svg>
                </button>
            )}
        </>
    );
};

export default ChatWidget;
4. Frontend Styling (ChatWidget.module.css)
This CSS file provides a modern, clean look for the chat widget.

/* General Style Improvements */
.chatToggleButton {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #3f51b5; /* Deep Indigo */
    color: white;
    border: none;
    border-radius: 50%; /* Make it a circle */
    width: 60px;
    height: 60px;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: transform 0.2s ease-in-out;
}

.chatToggleButton:hover {
    transform: scale(1.1);
}

.chatWindow {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 370px;
    height: 550px;
    background-color: #ffffff;
    border-radius: 15px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    display: flex;
    flex-direction: column;
    z-index: 1000;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.chatHeader {
    background: #1a1a1a;
    color: white;
    padding: 16px 20px;
    font-size: 18px;
    font-weight: 600;
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.closeButton {
    background: none;
    border: none;
    color: #a0a0a0;
    font-size: 24px;
    cursor: pointer;
    transition: color 0.2s;
}
.closeButton:hover {
    color: white;
}

.chatBody {
    flex-grow: 1;
    padding: 20px 10px;
    overflow-y: auto;
    background-color: #f9f9f9;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.welcomeMessage {
    text-align: center;
    color: #777;
    margin: auto;
    font-style: normal;
    font-size: 14px;
}

.message {
    padding: 10px 15px;
    border-radius: 18px;
    max-width: 85%;
    line-height: 1.5;
    word-wrap: break-word;
}

.user {
    align-self: flex-end;
    background-color: #007aff;
    color: white;
    border-bottom-right-radius: 4px;
}

.bot {
    align-self: flex-start;
    background-color: #e5e5ea;
    color: #1a1a1a;
    border-bottom-left-radius: 4px;
}

.chatInputForm {
    display: flex;
    align-items: center;
    border-top: 1px solid #e0e0e0;
    padding: 12px;
    background-color: #f0f0f0;
}

.chatInputForm input {
    flex-grow: 1;
    border: none;
    border-radius: 20px;
    padding: 12px 18px;
    margin-right: 10px;
    font-size: 15px;
    background-color: #ffffff;
}

.chatInputForm input:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(0, 122, 255, 0.3);
}

.chatInputForm button {
    background-color: #007aff;
    color: white;
    border: none;
    border-radius: 50%;
    width: 44px;
    height: 44px;
    cursor: pointer;
    font-size: 18px;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: background-color 0.2s;
    flex-shrink: 0;
}

.chatInputForm button:hover {
    background-color: #0056b3;
}

.chatInputForm button:disabled {
    background-color: #b0d7ff;
    cursor: not-allowed;
}

/* Modern Loading Dots (three bouncing balls) */
.loadingDots {
    display: flex;
    gap: 4px;
    align-items: center;
    padding: 10px 0;
}
.loadingDots span {
    width: 8px;
    height: 8px;
    background-color: #999;
    border-radius: 50%;
    animation: bounce 1.4s infinite both;
}
.loadingDots span:nth-child(2) {
    animation-delay: -0.32s;
}
.loadingDots span:nth-child(3) {
    animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1.0);
  }
}
5. System Prompt (aibo.md)
This file provides the core instructions for the AI model. It should be present in the same directory as main.py.

gemini --specifyplus aibo.md indexing_script.py main.py ChatWidget.js
**URGENT TASK: Generate Comprehensive RAG Chatbot Code and Instructions using specifyplus**

Mera maqsad Docusaurus book par RAG chatbot lagana hai. Mujhe teen files chahiye aur in files ki generation mein Google GenAI SDKs, Qdrant Cloud, aur FastAPI ka use karna lazmi hai.

**SPECIFYPLUS HIDAYAT:**
Iss request ko pura karne ke liye, Gemini ko 'specifyplus' ka istemal karte hue neeche di gayi teen files ko generate karna hai. Har file mein code ke saath-saath zaroori comments aur placeholders bhi hone chahiye.

**FILE GENERATION REQUIREMENTS:**

1.  **File: `indexing_script.py` (Python)**
    *   **Purpose:** Docusaurus Markdown files ko load, 500-character chunks mein todna, aur Qdrant mein vectors store karna.
    *   **Source Path:** `./AI-native-book/docs/`
    *   **Chunking:** 500-character split size, overlap 50 characters.
    *   **Qdrant Details:**
        *   URL: `https://63e9de2a-8a61-4e24-a204-ec23d83e394e.us-east4-0.gcp.cloud.qdrant.io`
        *   API Key: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.g4YrQIS00Km_6PgkHuP_r4te_zqkXNWxZJBhCkymtNA`
        *   Collection: `docusaurus_book_rag`
    *   **Embedding Model:** `text-embedding-004` (Google GenAI SDK se). Environment variable `GEMINI_API_KEY` use karein.

2.  **File: `main.py` (Python/FastAPI)**
    *   **Purpose:** RAG Backend API for chat.
    *   **Endpoint:** POST `/chat`
    *   **Logic:** Qdrant se retrieval (top_k=3) aur phir `gemini-2.5-flash` se generation.
    *   **Configuration:** CORS (Cross-Origin Resource Sharing) must be enabled for all origins (`*`) for easy frontend integration.

3.  **File: `ChatWidget.js` (React/JavaScript)**
    *   **Purpose:** Docusaurus component for a floating chat UI.
    *   **Functionality:** API call to the `/chat` endpoint on FastAPI server (assume it runs on `http://localhost:8000`).
    *   **UX:** Simple input field, send button, aur conversation history display ho.

**OUTPUT AND NEXT STEPS (CRUCIAL):**

Code files generate karne ke baad, **Gemini ko ek alag section mein Roman Urdu mein step-by-step instructions likhni hain** ki user ko yeh files generate hone ke baad kya karna hai, jismein yeh shamil ho:

1.  Zaroori Python dependencies install karna.
2.  `GEMINI_API_KEY` environment variable set karna.
3.  `indexing_script.py` chala kar data load karna.
4.  `main.py` (FastAPI) server start karna.
5.  `ChatWidget.js` ko Docusaurus mein kahan aur kaise embed karna hai (import aur use ka tareeqa).
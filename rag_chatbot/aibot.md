gemini --specifyplus aibo.md indexing_script.py main.py ChatWidget.js
**URGENT TASK: Generate Comprehensive RAG Chatbot Code and Instructions using specifyplus**

Mera maqsad Docusaurus book par RAG chatbot lagana hai. Mujhe teen files chahiye aur in files ki generation mein Google GenAI SDKs, Qdrant Cloud, aur FastAPI ka use karna lazmi hai.

**SPECIFYPLUS HIDAYAT:**
Iss request ko pura karne ke liye, Gemini ko 'specifyplus' ka istemal karte hue neeche di gayi teen files ko generate karna hai. Har file mein code ke saath-saath zaroori comments aur placeholders bhi hone chahiye.

**FILE GENERATION REQUIREMENTS:**

1.  **File: `indexing_script.py` (Python)**
    * **Purpose:** Docusaurus Markdown files ko load, 500-character chunks mein todna, aur Qdrant mein vectors store karna.
    * **Source Path:** `./AI-native-book/docs/`
    * **Chunking:** 500-character split size, overlap 50 characters.
    * **Qdrant Details:**
        * URL: `https://173afb85-1ba2-4c8e-98d2-e0da69faa82d.us-east4-0.gcp.cloud.qdrant.io:6333`
        * API Key: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.xq5gfyyq5JYP0kVFagk9iWUj9LxqigYO2IqqGr-Zu04`
        * Collection: `hummanoid_ai_book`
    * **Embedding Model:** `text-embedding-004` (Google GenAI SDK se). Environment variable `GEMINI_API_KEY` use karein.

2.  **File: `main.py` (Python/FastAPI)**
    * **Purpose:** RAG Backend API for chat.
    * **Endpoint:** POST `/chat`
    * **Logic:** Qdrant se retrieval (top_k=3) aur phir `gemini-2.5-flash` se generation.
    * **Configuration:** CORS (Cross-Origin Resource Sharing) must be enabled for all origins (`*`) for easy frontend integration.

3.  **File: `ChatWidget.js` (React/JavaScript)**
    * **Purpose:** Docusaurus component for a floating chat UI.
    * **Functionality:** API call to the `/chat` endpoint on FastAPI server (assume it runs on `http://localhost:8000`).
    * **UX:** Simple input field, send button, aur conversation history display ho.

**OUTPUT AND NEXT STEPS (CRUCIAL):**

Code files generate karne ke baad, **Gemini ko ek alag section mein Roman Urdu mein step-by-step instructions likhni hain** ki user ko yeh files generate hone ke baad kya karna hai, jismein yeh shamil ho:

1.  Zaroori Python dependencies install karna.
2.  `GEMINI_API_KEY` environment variable set karna.
3.  `indexing_script.py` chala kar data load karna.
4.  `main.py` (FastAPI) server start karna.
5.  `ChatWidget.js` ko Docusaurus mein kahan aur kaise embed karna hai (import aur use ka tareeqa).
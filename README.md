# AI Document Chat (Local RAG Implementation)

A fully localized Retrieval-Augmented Generation (RAG) application designed to allow semantic querying of PDF and text documents without relying on external APIs. 

This project demonstrates core Agentic AI principles by orchestrating document ingestion, vector embeddings, semantic search, and generative answering entirely on local compute resources.

## System Architecture

The application pipeline is broken down into four distinct micro-processes:

1. **Document Loading (`src/document_loader.py`):** Ingests raw `.pdf` or `.txt` files and applies text chunking strategies to optimize the data for vectorization.
2. **Embeddings (`src/embeddings.py`):** Utilizes `sentence-transformers` (all-MiniLM-L6-v2) to convert text chunks into high-dimensional vector representations.
3. **Vector Store (`src/vector_store.py`):** Implements FAISS (Facebook AI Similarity Search) to index the embeddings, enabling low-latency semantic similarity retrieval.
4. **Generation (`src/chatbot.py`):** Orchestrates the RAG loop. The queried context is retrieved from FAISS and passed to a local LLM (`google/flan-t5-base` via Transformers) to synthesize a deterministic, source-backed answer.

## Tech Stack
*   **Vector Search:** FAISS
*   **Embeddings:** Sentence-Transformers
*   **LLM Inference:** Hugging Face Transformers
*   **Interface:** Streamlit / CLI

## Installation & Setup

This application is designed to run locally without GPU requirements. 

**1. Clone the repository & create environment:**
```bash
git clone [https://github.com/Amr-Moussa-Ibrahim/ai-document-chat.git](https://github.com/Amr-Moussa-Ibrahim/ai-document-chat.git)
cd ai-document-chat
python -m venv venv

# Privacy-First Corporate Knowledge Base (Local RAG)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Ollama](https://img.shields.io/badge/LLM-Ollama%20%2F%20Llama%203.2-orange.svg)](https://ollama.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade, fully local Retrieval-Augmented Generation (RAG) system designed for secure corporate knowledge management. This application allows organizations to ingest massive proprietary PDFs (such as HR policies, compliance frameworks, or labor laws) and extract context-aware answers with **exact page-number citations**—all while operating 100% offline to ensure absolute data sovereignty.

---

## Key Features

* **100% On-Premise & Air-Gapped:** Zero data leaves your local network. Powered by local embeddings and open-source LLMs via Ollama.
* **Dynamic Document Lifecycle:** Drag-and-drop web UI allows non-technical users to upload new documentation, which completely flushes and rebuilds the vector space on-the-fly.
* **Deterministic Source Citations:** Eradicates standard LLM hallucinations by forcing the generator to cite the exact PDF page numbers where the underlying context was retrieved.
* **Smart Context Splitting:** Employs a recursive character textual chunker with rolling overlap metrics to maintain semantic context boundaries.

---

## Technical Architecture

This application bypasses traditional external API limitations by keeping the data ingestion, embedding generation, vector matching, and response compilation strictly on the local hardware layer.

```text
[User Query] ──> [HuggingFace Embeddings] ──> [Semantic Search in ChromaDB]
                                                          │
                                                (Top-K Context Chunks)
                                                          │
[User Query] + [Context + Page Metadata] ───────────────> [Local Llama 3.2] ──> [Streamlit Chat UI]

```

## Technology Stack

* **Orchestration:** LangChain
* **Vector Database:** ChromaDB
* **Local LLM Engine:** Ollama (Llama 3.2 Model)
* **Embedding Model:** HuggingFace Transformers (`all-MiniLM-L6-v2`)
* **User Interface:** Streamlit (Python Native UI)

---

## Installation & Setup

Ensure you have [Ollama](https://ollama.com/) installed and running on your local machine before starting.

### 1. Initialize the Local LLM
Pull the lightweight, production-tuned Llama 3.2 model to your local machine:

```bash
  ollama run llama3.2
```

### 2. Clone and Environment Setup

```bash
  git clone [https://github.com/YOUR_USERNAME/corporate-rag-kb.git](https://github.com/YOUR_USERNAME/corporate-rag-kb.git)
cd corporate-rag-kb 
```
### 3. Install Dependencies
```bash
  python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Usage guide

```bash
  streamlit run app.py
```
# Document Q&A Bot using RAG

## Overview

A Retrieval Augmented Generation (RAG) system that answers questions from PDF and DOCX documents.

## Features

- PDF support
- DOCX support
- Semantic Search
- ChromaDB persistent storage
- Gemini embeddings
- Grounded answers
- Source citations
- Streamlit UI

## Tech Stack

- Python
- Gemini API
- ChromaDB
- Streamlit
- PyPDF
- Python-docx

## Setup

### Clone Repository

```bash
git clone <repo_url>
cd document-qa-bot
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Add API Key

Create `.env`

```env
GEMINI_API_KEY=your_key
```

### Ingest Documents

```bash
cd src
python ingest.py
```

### Run App

```bash
streamlit run main.py
```

---

## Architecture

User Query
↓
ChromaDB Similarity Search
↓
Retrieve Top-k Chunks
↓
Prompt Engineering
↓
Gemini LLM
↓
Grounded Answer with Citations
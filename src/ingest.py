import os
import uuid
from pypdf import PdfReader
from docx import Document
from tqdm import tqdm

import chromadb
from chromadb.utils import embedding_functions
from config import *


# ---------------------------------------------------
# PDF Extraction
# ---------------------------------------------------

def extract_pdf(file_path):

    pages = []

    reader = PdfReader(file_path)

    for idx, page in enumerate(reader.pages):

        text = page.extract_text()

        if text and text.strip():

            pages.append({
                "text": " ".join(text.split()),
                "metadata": {
                    "source": os.path.basename(file_path),
                    "page": idx + 1
                }
            })

    return pages


# ---------------------------------------------------
# DOCX Extraction
# ---------------------------------------------------

def extract_docx(file_path):

    doc = Document(file_path)

    text = "\n".join([para.text for para in doc.paragraphs])

    return [{
        "text": text,
        "metadata": {
            "source": os.path.basename(file_path),
            "page": 1
        }
    }]


# ---------------------------------------------------
# Read Documents
# ---------------------------------------------------

def load_documents(data_folder):

    docs = []

    for file in os.listdir(data_folder):

        path = os.path.join(data_folder, file)

        if file.endswith(".pdf"):
            docs.extend(extract_pdf(path))

        elif file.endswith(".docx"):
            docs.extend(extract_docx(path))

    return docs


# ---------------------------------------------------
# Recursive Chunking
# ---------------------------------------------------

def chunk_documents(documents):

    chunks = []

    for doc in documents:

        text = doc["text"]
        metadata = doc["metadata"]

        start = 0

        while start < len(text):

            end = min(start + CHUNK_SIZE, len(text))

            chunk = text[start:end]

            chunks.append({
                "text": chunk,
                "metadata": {
                    **metadata,
                    "chunk_start": start,
                    "chunk_end": end
                }
            })

            start += (CHUNK_SIZE - CHUNK_OVERLAP)

    return chunks


# ---------------------------------------------------
# Save to ChromaDB
# ---------------------------------------------------

def save_to_chroma(chunks):

    client = chromadb.PersistentClient(path=DB_PATH)

    embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )

    ids = []
    texts = []
    metadatas = []

    for chunk in chunks:
        ids.append(str(uuid.uuid4()))
        texts.append(chunk["text"])
        metadatas.append(chunk["metadata"])

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas
    )

    print(f"{len(chunks)} chunks stored successfully.")


if __name__ == "__main__":

    print("Loading documents...")

    docs = load_documents("../data")

    print(f"Loaded {len(docs)} pages")

    chunks = chunk_documents(docs)

    print(f"Generated {len(chunks)} chunks")

    save_to_chroma(chunks)

    print("Ingestion completed.")
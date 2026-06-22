import google.generativeai as genai
import chromadb

from chromadb.utils import embedding_functions
from config import *

genai.configure(api_key=GEMINI_API_KEY)


def retrieve_context(question):

    client = chromadb.PersistentClient(path=DB_PATH)

    embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_collection(
        COLLECTION_NAME,
        embedding_function=embedding_fn
    )

    results = collection.query(
        query_texts=[question],
        n_results=TOP_K
    )

    contexts = []

    for doc, meta in zip(
            results["documents"][0],
            results["metadatas"][0]):

        contexts.append(
            f"""
            [Source: {meta['source']} | Page: {meta['page']}]

            {doc}
            """
        )

    return "\n\n".join(contexts)


def ask_question(question):

    context = retrieve_context(question)

    prompt = f"""
You are an expert Document Question Answering Assistant.

RULES:
1. Answer ONLY from the provided context.
2. Cite sources.
3. If answer unavailable say:
   "I cannot find the answer in the provided documents."
4. Never hallucinate.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    return response.text
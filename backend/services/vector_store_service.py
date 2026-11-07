
import chromadb

from pathlib import Path


# Persistent database directory
CHROMA_DIR = Path("./chroma_db")

COLLECTION_NAME = "cogniflow_policies"


# Create ChromaDB client
client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)


# Create or retrieve collection
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={
        "description": "Cogniflow company policy documents"
    },
)


def store_policy_chunks(chunks):

    if not chunks:
        raise ValueError("No policy chunks provided.")

    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        ids.append(
            f"{chunk['source']}_{chunk['chunk_id']}"
        )

        documents.append(
            chunk["content"]
        )

        metadatas.append({
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
        })

    # Upsert prevents duplicate records on repeated ingestion
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    return collection.count()


def search_policy_chunks(query, top_k=3):

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count()),
    )

    return results

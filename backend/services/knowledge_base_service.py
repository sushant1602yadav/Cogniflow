
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


# Path to the knowledge base folder
KNOWLEDGE_BASE_DIR = Path("knowledge_base")


def load_policy_documents():

    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.glob("*.txt"):

        content = file_path.read_text(
            encoding="utf-8"
        )

        documents.append({
            "source": file_path.name,
            "content": content,
        })

    return documents


def split_policy_documents(
    documents,
    chunk_size=500,
    chunk_overlap=100,
):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = []

    for document in documents:

        split_texts = text_splitter.split_text(
            document["content"]
        )

        for index, text in enumerate(split_texts):

            chunks.append({
                "source": document["source"],
                "chunk_id": index,
                "content": text,
            })

    return chunks

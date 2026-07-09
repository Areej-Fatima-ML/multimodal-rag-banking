import chromadb
from app.config.settings import CHROMA_DB_PATH, COLLECTION_NAME


# Global client and collection variables - initialized once
_client = None
_collection = None


def get_client():
    """
    Get or create ChromaDB persistent client
    PersistentClient saves data to disk automatically
    Returns ChromaDB client instance
    """
    global _client

    if _client is None:
        print("Connecting to ChromaDB...")
        # PersistentClient saves data to disk
        _client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        print("ChromaDB connected!")

    return _client


def get_collection():
    """
    Get or create ChromaDB collection
    Uses cosine similarity for semantic search
    Returns ChromaDB collection instance
    """
    global _collection

    if _collection is None:
        client = get_client()
        # get_or_create ensures we dont lose existing data
        _collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

    return _collection


def store_chunks(chunks: list, embeddings: list) -> bool:
    """
    Store text chunks and embeddings in ChromaDB
    Stores in batches to avoid size limits
    Also stores metadata for each chunk
    Returns True if successful
    """
    collection = get_collection()

    ids = []
    documents = []
    metadatas = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        # Create unique ID for each chunk
        chunk_id = f"chunk_{i}_{chunk['metadata'].get('source', 'unknown')}"
        # Clean ID - remove special characters
        chunk_id = chunk_id.replace("\\", "_").replace("/", "_").replace(".", "_")

        ids.append(chunk_id)
        documents.append(chunk["content"])
        metadatas.append({
            "source": chunk["metadata"].get("source", "unknown"),
            "type": chunk["metadata"].get("type", "text"),
            "page": str(chunk["metadata"].get("page", 0)),
            "slide": str(chunk["metadata"].get("slide", 0)),
            "chunk_index": str(chunk.get("chunk_index", i))
        })

    # Store in batches of 5000 to avoid ChromaDB limit
    batch_size = 5000
    for i in range(0, len(ids), batch_size):
        batch_ids = ids[i:i + batch_size]
        batch_docs = documents[i:i + batch_size]
        batch_meta = metadatas[i:i + batch_size]
        batch_emb = embeddings[i:i + batch_size]

        collection.add(
            ids=batch_ids,
            documents=batch_docs,
            embeddings=batch_emb,
            metadatas=batch_meta
        )
        print(f"Stored batch {i // batch_size + 1}!")

    print(f"Total {len(chunks)} chunks stored in ChromaDB!")
    return True


def search_similar(query_embedding: list, top_k: int = 5) -> list:
    """
    Search for most similar chunks using cosine similarity
    Returns top K most relevant chunks with scores
    """
    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    # Format results with similarity scores
    similar_chunks = []
    for i in range(len(results["documents"][0])):
        similar_chunks.append({
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            # Convert distance to similarity score
            "score": round(1 - results["distances"][0][i], 4)
        })

    return similar_chunks


def get_collection_count() -> int:
    """
    Get total number of chunks stored in ChromaDB
    Returns integer count
    """
    collection = get_collection()
    return collection.count()


def collection_exists() -> bool:
    """
    Check if collection already has data
    Used to avoid re-ingestion
    Returns True if collection has data
    """
    try:
        count = get_collection_count()
        return count > 0
    except:
        return False
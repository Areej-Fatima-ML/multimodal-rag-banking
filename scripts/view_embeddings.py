import chromadb
import json
from app.config.settings import CHROMA_DB_PATH, COLLECTION_NAME


def view_embeddings(num_samples: int = 5):
    """
    View stored embeddings from ChromaDB
    Shows document text, metadata and vector values
    Used for demonstrating embeddings in interviews
    """
    # Connect to ChromaDB
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_collection(COLLECTION_NAME)

    # Get sample documents with embeddings
    results = collection.get(
        limit=num_samples,
        include=["embeddings", "documents", "metadatas"]
    )

    print("\n" + "="*60)
    print("CHROMADB EMBEDDINGS VIEWER")
    print("="*60)
    print(f"Total chunks stored: {collection.count()}")
    print(f"Embedding dimensions: 384")
    print(f"Similarity metric: Cosine")
    print("="*60)

    # Display each sample
    for i in range(len(results['documents'])):
        print(f"\n--- Chunk {i+1} ---")
        print(f"Source:   {results['metadatas'][i].get('source', 'unknown')}")
        print(f"Type:     {results['metadatas'][i].get('type', 'text')}")
        print(f"Page:     {results['metadatas'][i].get('page', 'N/A')}")
        print(f"Text:     {results['documents'][i][:150]}...")
        print(f"Vector:   {results['embeddings'][i][:10]}")
        print(f"Size:     {len(results['embeddings'][i])} dimensions")
        print("-"*60)

    print("\n✅ Embeddings are stored and working!")
    print(f"✅ Total {collection.count()} chunks ready for search!")


def search_demo(query: str = "What are AML regulations?"):
    """
    Demo search to show how embeddings work
    Shows query embedding vs stored embeddings
    """
    from app.embeddings.embedder import get_single_embedding
    from app.vectorstore.chroma_store import search_similar

    print(f"\n{'='*60}")
    print("SEARCH DEMO")
    print(f"{'='*60}")
    print(f"Query: {query}")

    # Get query embedding
    query_embedding = get_single_embedding(query)
    print(f"\nQuery Vector (first 10): {query_embedding[:10]}")

    # Search similar chunks
    results = search_similar(query_embedding, top_k=3)

    print(f"\nTop 3 Similar Chunks:")
    for i, chunk in enumerate(results):
        print(f"\n{i+1}. Score: {chunk['score']}")
        print(f"   Source: {chunk['metadata'].get('source', 'unknown')}")
        print(f"   Text: {chunk['content'][:100]}...")


if __name__ == "__main__":
    # View stored embeddings
    view_embeddings(num_samples=5)

    # Demo search
    search_demo("What are AML regulations?")
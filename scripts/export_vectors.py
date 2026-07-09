import chromadb
from app.config.settings import CHROMA_DB_PATH, COLLECTION_NAME

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_collection(COLLECTION_NAME)

# Get vectors directly from ChromaDB
results = collection.get(
    limit=5,
    include=["embeddings", "documents", "metadatas"]
)

print("\n=== VECTORS FROM CHROMADB ===")
print(f"Total stored: {collection.count()}")

for i in range(len(results['documents'])):
    print(f"\n--- Chunk {i+1} ---")
    print(f"Source: {results['metadatas'][i].get('source', 'unknown')}")
    print(f"Text: {results['documents'][i][:80]}...")
    print(f"Vector (all 384 values):")
    print(results['embeddings'][i])
    print(f"Vector size: {len(results['embeddings'][i])}")
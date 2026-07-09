import chromadb
import json
from app.config.settings import CHROMA_DB_PATH, COLLECTION_NAME

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_collection(COLLECTION_NAME)

# Get embeddings
results = collection.get(
    limit=10,
    include=["embeddings", "documents", "metadatas"]
)

# Save to readable JSON file
vectors_data = []
for i in range(len(results['documents'])):
    vectors_data.append({
        "chunk_id": i + 1,
        "source": results['metadatas'][i].get('source', 'unknown'),
        "type": results['metadatas'][i].get('type', 'text'),
        "text": results['documents'][i][:100],
        "vector_size": len(results['embeddings'][i]),
        # Convert numpy array to list
        "vector": results['embeddings'][i].tolist()
    })

# Save to JSON file
with open('./data/embeddings_sample.json', 'w') as f:
    json.dump(vectors_data, f, indent=4)

print(" Vectors saved to data/embeddings_sample.json!")
print(f"Total vectors saved: {len(vectors_data)}")
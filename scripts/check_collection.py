import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import chromadb
from app.config.settings import CHROMA_DB_PATH, COLLECTION_NAME

print("="*60)
print("COLLECTION NAME CHECK")
print("="*60)
print(f"Settings mein Collection Name: {COLLECTION_NAME}")

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

print(f"\nChromaDB Path: {CHROMA_DB_PATH}")
print("Available Collections:")

collections = client.list_collections()
if collections:
    for col in collections:
        print(f" - {col.name}  ({col.count} chunks)")
else:
    print(" - No collections found")

print("\n" + "="*60)
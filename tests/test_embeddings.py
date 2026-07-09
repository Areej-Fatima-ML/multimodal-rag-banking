from app.embeddings.embedder import get_embeddings, get_single_embedding
from app.vectorstore.chroma_store import get_collection_count


def test_embeddings():
    """
    Test embedding generation
    """
    print("\n=== Testing Embeddings ===")

    # Test single embedding
    text = "What are AML regulations?"
    embedding = get_single_embedding(text)

    print(f" Single embedding generated")
    print(f"   Vector size: {len(embedding)}")
    print(f"   First 5 values: {embedding[:5]}")

    # Test batch embeddings
    texts = [
        "AML regulations",
        "Digital banking",
        "Loan eligibility"
    ]
    embeddings = get_embeddings(texts)

    print(f" Batch embeddings generated")
    print(f"   Total: {len(embeddings)}")
    print(f"   Each size: {len(embeddings[0])}")

    # Test ChromaDB count
    count = get_collection_count()
    print(f" ChromaDB chunks: {count}")

    print("\n All embedding tests passed!")


if __name__ == "__main__":
    test_embeddings()
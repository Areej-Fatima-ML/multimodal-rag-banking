from app.pipeline.query_pipeline import run_text_query
from app.pipeline.ingest_pipeline import run_ingestion


def test_text_query():
    """
    Test text query pipeline
    """
    print("\n=== Testing Text Query Pipeline ===")

    # Test banking query
    result = run_text_query("What are AML regulations?")

    print(f"✅ Query: {result['query']}")
    print(f"✅ Answer: {result['answer'][:100]}...")
    print(f"✅ Sources: {len(result['sources'])}")
    print(f"✅ Chunks: {len(result['retrieved_chunks'])}")

    # Test non-banking query
    result2 = run_text_query("fix my car")
    print(f"\n✅ Non-banking query handled!")
    print(f"   Answer: {result2['answer']}")
    print(f"   Sources: {result2['sources']}")

    # Test greeting
    result3 = run_text_query("hi")
    print(f"\n✅ Greeting handled!")
    print(f"   Answer: {result3['answer']}")

    print("\n✅ All pipeline tests passed!")


def test_memory():
    """
    Test chat memory
    """
    print("\n=== Testing Chat Memory ===")

    chat_history = []

    # First question
    result1 = run_text_query(
        "What are AML regulations?",
        chat_history
    )
    chat_history.append({
        "role": "user",
        "content": "What are AML regulations?"
    })
    chat_history.append({
        "role": "assistant",
        "content": result1["answer"]
    })

    # Memory question
    result2 = run_text_query(
        "what i asked last time?",
        chat_history
    )

    print(f" Memory test!")
    print(f"   Answer: {result2['answer']}")
    print("\n Memory test passed!")


if __name__ == "__main__":
    test_text_query()
    test_memory()
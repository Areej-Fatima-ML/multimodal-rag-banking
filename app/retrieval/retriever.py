from app.embeddings.embedder import get_single_embedding
from app.vectorstore.chroma_store import search_similar
from app.config.settings import TOP_K_RESULTS


def retrieve_text_query(query: str, top_k: int = TOP_K_RESULTS) -> list:
    """
    Retrieve most relevant chunks for text query
    Converts query to embedding then searches ChromaDB
    """
    query_embedding = get_single_embedding(query)
    results = search_similar(query_embedding, top_k)
    return results


def retrieve_image_query(image_description: str, top_k: int = TOP_K_RESULTS) -> list:
    """
    Retrieve most relevant chunks for image query
    Image already converted to text description
    """
    query_embedding = get_single_embedding(image_description)
    results = search_similar(query_embedding, top_k)
    return results


def filter_relevant_chunks(chunks: list, min_score: float = 0.5) -> list:
    """
    Filter chunks by minimum similarity score
    Score 0.5+ = relevant
    Score below 0.5 = irrelevant
    """
    relevant = [
        chunk for chunk in chunks
        if chunk["score"] >= 0.5
    ]
    return relevant


def format_context(retrieved_chunks: list) -> str:
    """
    Format retrieved chunks as context for LLM
    Includes source name and page number
    """
    if not retrieved_chunks:
        return "No relevant context found."

    context = ""
    for i, chunk in enumerate(retrieved_chunks):
        source = chunk['metadata'].get('source', 'unknown')
        source_name = source.split("\\")[-1].split("/")[-1]
        chunk_type = chunk['metadata'].get('type', 'text')
        page = chunk['metadata'].get('page', 'N/A')
        score = chunk.get('score', 0)

        context += f"\n--- Source {i+1}: {source_name} "
        context += f"| Page: {page} "
        context += f"| Type: {chunk_type} "
        context += f"| Score: {score} ---\n"
        context += chunk["content"]
        context += "\n"

    return context
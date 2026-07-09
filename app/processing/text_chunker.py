from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config.settings import CHUNK_SIZE, CHUNK_OVERLAP


def create_chunks(text: str, metadata: dict) -> list:
    """
    Split a single text into smaller chunks
    Uses RecursiveCharacterTextSplitter for smart splitting
    Maintains context with chunk overlap
    Returns list of chunk dicts with content and metadata
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        # Try splitting by these separators in order
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = text_splitter.split_text(text)

    result = []
    for i, chunk in enumerate(chunks):
        # Skip empty chunks
        if chunk.strip():
            result.append({
                "content": chunk,
                "chunk_index": i,
                "metadata": metadata
            })

    return result


def chunk_documents(documents: list) -> list:
    """
    Chunk all extracted documents
    Processes text, table and image description content
    Returns list of all chunks with metadata
    """
    all_chunks = []

    for doc in documents:
        # Build metadata for each chunk
        metadata = {
            "source": doc.get("source", "unknown"),
            "type": doc.get("type", "text"),
            "page": doc.get("page", 0),
            "slide": doc.get("slide", 0)
        }

        # Create chunks from document content
        chunks = create_chunks(doc["content"], metadata)
        all_chunks.extend(chunks)

    return all_chunks
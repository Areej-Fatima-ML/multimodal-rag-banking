from sentence_transformers import SentenceTransformer
from app.config.settings import EMBEDDING_MODEL_NAME


# Global model variable - loaded once and reused
_model = None


def load_model() -> SentenceTransformer:
    """
    Load embedding model from HuggingFace
    Model is loaded only once and cached in memory
    Saves time on subsequent calls
    Returns SentenceTransformer model
    """
    global _model

    if _model is None:
        print(f"Loading embedding model...")
        # Download from HuggingFace
     
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        print("Embedding model loaded successfully!")

    return _model


def get_embeddings(texts: list) -> list:
    """
    Convert list of texts to embeddings
    Used during ingestion to store document embeddings
    Returns list of embedding vectors
    """
    model = load_model()

    # Encode all texts with progress bar
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        batch_size=32
    )

    return embeddings.tolist()


def get_single_embedding(text: str) -> list:
    """
    Convert single text to embedding
    Used during query time for search
    Returns single embedding vector
    """
    model = load_model()
    embedding = model.encode([text])
    return embedding[0].tolist()
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ─── Groq API Settings ───────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_TEXT_MODEL = "llama-3.1-8b-instant"
GROQ_VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# ─── Embedding Model Settings ────────────────────────────
# Model name for downloading from HuggingFace
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
# Local path where model is saved (inside Docker)
EMBEDDING_MODEL_PATH = "./models/embeddings/all-MiniLM-L6-v2"

# ─── ChromaDB Settings ───────────────────────────────────
# Path where ChromaDB stores data persistently
CHROMA_DB_PATH = "./chromadb_data"
# Collection name in ChromaDB
COLLECTION_NAME = "banking_docs"

# ─── Text Chunking Settings ──────────────────────────────
# Maximum characters per chunk
CHUNK_SIZE = 500
# Overlapping characters between chunks (maintains context)
CHUNK_OVERLAP = 50

# ─── Retrieval Settings ──────────────────────────────────
# Number of similar chunks to retrieve per query
TOP_K_RESULTS = 5

# ─── File Settings ───────────────────────────────────────
# Supported file extensions
ALLOWED_EXTENSIONS = [
    ".pdf", ".docx", ".pptx",
    ".jpg", ".jpeg", ".png"
]
# Path to banking documents
DATA_PATH = "./data/documents"
# Path for temporary uploads
UPLOAD_PATH = "./data/uploads"
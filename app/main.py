from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import ingest, query
import os

# Create FastAPI application
app = FastAPI(
    title="Multimodal Banking RAG System",
    description="""
    A RAG system for SBP banking documents.
    Supports both text and image queries.
    Built with FastAPI, ChromaDB and Groq LLaMA.
    """,
    version="1.0.0"
)

# Add CORS middleware
# Allows Streamlit UI to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(
    ingest.router,
    prefix="/api",
    tags=["Ingestion"]
)
app.include_router(
    query.router,
    prefix="/api",
    tags=["Query"]
)

# Create necessary directories on startup
@app.on_event("startup")
async def startup_event():
    """
    Create required directories when app starts
    """
    os.makedirs("./data/documents", exist_ok=True)
    os.makedirs("./data/uploads", exist_ok=True)
    os.makedirs("./chromadb_data", exist_ok=True)
    os.makedirs("./models/embeddings", exist_ok=True)
    print("Directories created!")
    print("Banking RAG System started!")


@app.get("/")
async def root():
    """
    Root endpoint - system status
    """
    return {
        "message": "Multimodal Banking RAG System",
        "status": "running",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """
    Health check endpoint
    Used by Docker to verify service is running
    """
    return {
        "status": "healthy",
        "service": "Banking RAG API"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
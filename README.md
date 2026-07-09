# SBP Multimodal Banking RAG System

A RAG system for State Bank of Pakistan banking documents that supports both text and image queries.

## What it does
- Answer questions from SBP banking documents using text queries
- Analyze banking charts and images using image queries
- Maintains chat history and memory
- Cites sources with page numbers

## Tech Stack
- LLM: Groq LLaMA 3.1 (text answers)
- Vision: LLaMA 4 Scout (image understanding)
- Embeddings: all-MiniLM-L6-v2 (local)
- Vector DB: ChromaDB
- Backend: FastAPI
- Frontend: Streamlit

## Project Structure
- `app/ingestion/` - File parsers for PDF, DOCX, PPTX, Images
- `app/processing/` - Text chunking and image description
- `app/embeddings/` - Embedding model
- `app/vectorstore/` - ChromaDB vector store
- `app/retrieval/` - Semantic search
- `app/generation/` - Answer generation
- `app/pipeline/` - Ingestion and query pipelines
- `app/api/` - FastAPI routes
- `ui/` - Streamlit interface
- `scripts/` - Utility scripts

## Setup

```bash
# Create environment
conda create -n banking-rag python=3.11 -y
conda activate banking-rag

# Install dependencies
pip install -r requirements.txt

# Add Groq API key to .env
GROQ_API_KEY=your_key_here

# Run ingestion
python -m app.pipeline.ingest_pipeline

# Start FastAPI
python -m uvicorn app.main:app --reload --port 8000

# Start Streamlit
streamlit run ui/streamlit_app.py
```

## API Endpoints
- `POST /api/ingest` - Ingest documents
- `POST /api/upload` - Upload new document
- `POST /api/query/text` - Text query
- `POST /api/query/image` - Image query


## Key Design Decisions
- Used LLaVA for accurate data extraction from banking charts
- All content converted to text before embedding for unified pipeline
- Groq API used for  cloud inference 

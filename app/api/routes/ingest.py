from fastapi import APIRouter, UploadFile, File
import shutil
import os
from app.pipeline.ingest_pipeline import run_ingestion
from app.api.schemas import IngestResponse, UploadResponse
from app.config.settings import UPLOAD_PATH, DATA_PATH

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
async def ingest_documents():
    """
    Ingest all documents from data/documents folder
    Processes PDFs, DOCX, PPTX and images
    Stores embeddings in ChromaDB
    """
    result = run_ingestion()

    return IngestResponse(
        status=result["status"],
        total_files=result["total_files"],
        total_chunks=result["total_chunks"],
        message=f"Successfully ingested {result['total_files']} files with {result['total_chunks']} chunks!"
    )


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a new document to data/documents folder
    Supports PDF, DOCX, PPTX and image files
    File will be available for next ingestion
    """
    # Create upload directory if not exists
    os.makedirs(DATA_PATH, exist_ok=True)

    # Save file to documents folder
    file_path = os.path.join(DATA_PATH, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return UploadResponse(
        status="success",
        filename=file.filename,
        message=f"{file.filename} uploaded successfully! Run ingestion to process it."
    )
from fastapi import APIRouter, UploadFile, File
import shutil
import os
from app.pipeline.query_pipeline import run_text_query, run_image_query
from app.api.schemas import TextQueryRequest, QueryResponse
from app.config.settings import UPLOAD_PATH

router = APIRouter()


@router.post("/query/text", response_model=QueryResponse)
async def text_query(request: TextQueryRequest):
    """
    Query banking documents using text
    Supports conversation memory via chat history
    Returns answer with sources
    """
    # Convert pydantic chat history to dict list
    chat_history = [
        {"role": msg.role, "content": msg.content}
        for msg in request.chat_history
    ]

    # Run text query pipeline
    result = run_text_query(request.query, chat_history)

    return QueryResponse(
        query=result["query"],
        answer=result["answer"],
        sources=result["sources"],
        status="success"
    )


@router.post("/query/image")
async def image_query(
    query: str,
    file: UploadFile = File(...)
):
    """
    Query banking documents using an image
    Image is described by LLaVA then used for search
    Returns answer with image description and sources
    """
    # Create upload directory if not exists
    os.makedirs(UPLOAD_PATH, exist_ok=True)

    # Save uploaded image temporarily
    image_path = os.path.join(UPLOAD_PATH, file.filename)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run image query pipeline
    result = run_image_query(image_path, query)

    # Clean up temporary image file
    if os.path.exists(image_path):
        os.remove(image_path)

    return {
        "query": result["query"],
        "answer": result["answer"],
        "image_description": result["image_description"],
        "sources": result["sources"],
        "status": "success"
    }
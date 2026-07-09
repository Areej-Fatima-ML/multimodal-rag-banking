from pydantic import BaseModel
from typing import List, Optional


class ChatMessage(BaseModel):
    """
    Single chat message model
    Used for maintaining conversation history
    """
    role: str  # 'user' or 'assistant'
    content: str


class TextQueryRequest(BaseModel):
    """
    Request model for text query endpoint
    Includes query and optional chat history
    """
    query: str
    chat_history: List[ChatMessage] = []


class QueryResponse(BaseModel):
    """
    Response model for query endpoints
    Returns answer, sources and status
    """
    query: str
    answer: str
    sources: List[str] = []
    status: str = "success"


class IngestResponse(BaseModel):
    """
    Response model for ingestion endpoint
    Returns ingestion status and statistics
    """
    status: str
    total_files: int
    total_chunks: int
    message: str


class UploadResponse(BaseModel):
    """
    Response model for file upload endpoint
    Returns upload status and filename
    """
    status: str
    filename: str
    message: str
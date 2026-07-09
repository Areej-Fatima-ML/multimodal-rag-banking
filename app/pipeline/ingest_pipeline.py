import json
import os
from app.ingestion.file_router import get_all_files
from app.ingestion.pdf_parser import parse_pdf
from app.ingestion.docx_parser import parse_docx
from app.ingestion.pptx_parser import parse_pptx
from app.ingestion.image_parser import parse_image
from app.processing.text_chunker import chunk_documents
from app.processing.image_describer import describe_all_images
from app.processing.table_extractor import extract_tables_from_pdf
from app.embeddings.embedder import get_embeddings
from app.vectorstore.chroma_store import store_chunks, get_collection_count, collection_exists
from app.config.settings import DATA_PATH

# Progress files for resume support
TEXTS_FILE = "./data/progress_texts.json"
CHUNKS_FILE = "./data/progress_chunks.json"
EMBEDDINGS_FILE = "./data/progress_embeddings.json"


def save_progress(data: list, filename: str):
    """
    Save progress to JSON file
    Allows resuming from last successful step
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"Progress saved: {filename}")


def load_progress(filename: str) -> list:
    """
    Load saved progress from JSON file
    Returns empty list if file does not exist
    """
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def clean_progress_files():
    """
    Remove progress files after successful ingestion
    """
    for f in [TEXTS_FILE, CHUNKS_FILE, EMBEDDINGS_FILE]:
        if os.path.exists(f):
            os.remove(f)
    print("Progress files cleaned!")


def process_file(file_info: dict) -> dict:
    """
    Process single file based on its type
    Extracts text, tables and images from each file
    Returns dict with all extracted content
    """
    file_type = file_info["file_type"]
    file_path = file_info["file_path"]

    all_texts = []
    all_images = []

    if file_type == "pdf":
        # Parse PDF - extract text and images
        result = parse_pdf(file_path)
        all_texts.extend(result["texts"])
        all_images.extend(result["images"])

        # Extract tables separately from PDF
        tables = extract_tables_from_pdf(file_path)
        all_texts.extend(tables)

    elif file_type == "docx":
        # Parse Word document
        result = parse_docx(file_path)
        all_texts.extend(result["texts"])
        all_texts.extend(result["tables"])
        all_images.extend(result["images"])

    elif file_type == "pptx":
        # Parse PowerPoint presentation
        result = parse_pptx(file_path)
        all_texts.extend(result["texts"])
        all_texts.extend(result["tables"])
        all_images.extend(result["images"])

    elif file_type == "image":
        # Parse standalone image
        result = parse_image(file_path)
        all_images.append({
            "image": result["image"],
            "source": file_path
        })

    return {
        "texts": all_texts,
        "images": all_images,
        "file_path": file_path
    }


def run_ingestion(data_path: str = DATA_PATH) -> dict:
    """
    Run complete ingestion pipeline with resume support
    Steps:
    1. Get all files
    2. Parse files - extract text and images
    3. Describe images with LLaVA
    4. Chunk all texts
    5. Generate embeddings
    6. Store in ChromaDB
    Saves progress after each step for resume support
    """
    print("\n" + "="*50)
    print("STARTING INGESTION PIPELINE")
    print("="*50)

    # ─── STEP 1: Get all files ───────────────────────
    print("\nStep 1: Getting all files...")
    files = get_all_files(data_path)
    print(f"Found {len(files)} files!")

    # ─── STEP 2 & 3: Process + Describe images ───────
    # Try to load saved progress first
    all_texts = load_progress(TEXTS_FILE)

    if all_texts:
        print(f"\nStep 2&3: Resuming! {len(all_texts)} texts already saved!")
    else:
        print("\nStep 2: Processing files...")
        raw_texts = []
        all_images = []

        for file_info in files:
            print(f"Processing: {file_info['file_name']}")
            result = process_file(file_info)
            raw_texts.extend(result["texts"])
            all_images.extend(result["images"])

        print(f"\nTotal texts extracted: {len(raw_texts)}")
        print(f"Total images extracted: {len(all_images)}")

        # Describe images with LLaVA vision model
        print("\nStep 3: Describing images with LLaVA...")
        if all_images:
            image_descriptions = describe_all_images(all_images)
            raw_texts.extend(image_descriptions)
            print(f"Total image descriptions: {len(image_descriptions)}")

        # Convert to serializable format for saving
        all_texts = []
        for t in raw_texts:
            all_texts.append({
                "content": t.get("content", ""),
                "type": t.get("type", "text"),
                "source": t.get("source", "unknown"),
                "page": t.get("page", 0),
                "slide": t.get("slide", 0)
            })

        # Save progress
        save_progress(all_texts, TEXTS_FILE)

    # ─── STEP 4: Chunking ────────────────────────────
    all_chunks = load_progress(CHUNKS_FILE)

    if all_chunks:
        print(f"\nStep 4: Resuming! {len(all_chunks)} chunks already saved!")
    else:
        print("\nStep 4: Chunking texts...")
        all_chunks = chunk_documents(all_texts)
        print(f"Total chunks created: {len(all_chunks)}")
        save_progress(all_chunks, CHUNKS_FILE)

    # ─── STEP 5: Embeddings ──────────────────────────
    all_embeddings = load_progress(EMBEDDINGS_FILE)

    if all_embeddings:
        print(f"\nStep 5: Resuming! {len(all_embeddings)} embeddings already saved!")
    else:
        print("\nStep 5: Generating embeddings...")
        texts_only = [chunk["content"] for chunk in all_chunks]
        all_embeddings = get_embeddings(texts_only)
        print(f"Total embeddings created: {len(all_embeddings)}")
        save_progress(all_embeddings, EMBEDDINGS_FILE)

    # ─── STEP 6: Store in ChromaDB ───────────────────
    print("\nStep 6: Storing in ChromaDB...")
    store_chunks(all_chunks, all_embeddings)

    total_stored = get_collection_count()

    # Clean up progress files after success
    clean_progress_files()

    print("\n" + "="*50)
    print("INGESTION COMPLETE!")
    print(f"Total chunks stored: {total_stored}")
    print("="*50)

    return {
        "status": "success",
        "total_files": len(files),
        "total_chunks": total_stored
    }


if __name__ == "__main__":
    run_ingestion()
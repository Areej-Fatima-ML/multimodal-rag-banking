import fitz  # PyMuPDF library for PDF processing
import io
from PIL import Image


def extract_text_from_pdf(file_path: str) -> list:
    """
    Extract all text content from PDF file
    Returns list of text dicts with content, page number and source
    """
    texts = []
    doc = fitz.open(file_path)

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()

        # Only add non-empty text
        if text.strip():
            texts.append({
                "content": text,
                "page": page_num + 1,
                "type": "text",
                "source": file_path
            })

    doc.close()
    return texts


def extract_images_from_pdf(file_path: str) -> list:
    """
    Extract all embedded images from PDF file
    Returns list of image dicts with PIL image object and metadata
    """
    images = []
    doc = fitz.open(file_path)

    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images()

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))

            
            if image.width >= 10 and image.height >= 10:
                images.append({
                    "image": image,
                    "page": page_num + 1,
                    "index": img_index,
                    "type": "image",
                    "source": file_path
                })

    doc.close()
    return images


def parse_pdf(file_path: str) -> dict:
    """
    Parse complete PDF file
    Extracts both text and images
    Returns dict with texts, images and metadata
    """
    texts = extract_text_from_pdf(file_path)
    images = extract_images_from_pdf(file_path)

    return {
        "file_path": file_path,
        "texts": texts,
        "images": images,
        "total_pages": len(fitz.open(file_path)),
        "total_images": len(images)
    }
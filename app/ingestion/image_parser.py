import base64
import io
from PIL import Image


def load_image(file_path: str) -> Image.Image:
    """
    Load image from file path
    Returns PIL Image object
    """
    image = Image.open(file_path)
    return image


def image_to_base64(image: Image.Image) -> str:
    """
    Convert PIL image to base64 encoded string
    Required format for Groq LLaVA vision API
    Returns base64 string
    """
    buffered = io.BytesIO()

    # Convert to RGB if image has alpha channel or different mode
    if image.mode != "RGB":
        image = image.convert("RGB")

    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return img_base64


def is_valid_image(image: Image.Image) -> bool:
    """
    Check if image meets minimum size requirements
    LLaVA requires at least 10x10 pixels
    Returns True if image is valid
    """
    return image.width >= 10 and image.height >= 10


def parse_image(file_path: str) -> dict:
    """
    Parse standalone image file
    Loads image and converts to base64 for LLaVA
    Returns dict with image object, base64 and metadata
    """
    image = load_image(file_path)

    # Convert to base64 for API
    img_base64 = image_to_base64(image)

    return {
        "file_path": file_path,
        "image": image,
        "base64": img_base64,
        "width": image.width,
        "height": image.height,
        "type": "image",
        "source": file_path
    }
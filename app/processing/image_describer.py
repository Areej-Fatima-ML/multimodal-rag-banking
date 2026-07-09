import base64
import io
from PIL import Image
from groq import Groq
from app.config.settings import GROQ_API_KEY, GROQ_VISION_MODEL


def image_to_base64(image: Image.Image) -> str:
    """
    Convert PIL image to base64 encoded string
    Required format for Groq vision API
    Returns base64 string
    """
    buffered = io.BytesIO()

    # Convert to RGB if needed
    if image.mode != "RGB":
        image = image.convert("RGB")

    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def is_valid_image(image: Image.Image) -> bool:
    """
    Check if image meets minimum size requirements
    Returns True if image is valid for processing
    """
    return image.width >= 10 and image.height >= 10


def describe_image(image: Image.Image, source: str = "") -> dict:
    """
    Send image to LLaVA vision model via Groq API
    Gets detailed text description of image content
    Handles charts, tables, graphs and regular images
    Returns dict with description and metadata
    """
    # Skip invalid images
    if not is_valid_image(image):
        return {
            "content": "Image too small to process",
            "type": "image_description",
            "source": source
        }

    client = Groq(api_key=GROQ_API_KEY)
    img_base64 = image_to_base64(image)

    try:
        response = client.chat.completions.create(
            model=GROQ_VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": """You are a banking document analyst.
Analyze this image carefully and provide a detailed description.

If it contains:
- Charts or graphs: Extract all data points, trends, labels and numbers
- Tables: Extract all rows, columns and values
- Text: Extract the complete text content
- Diagrams: Describe the structure and key components

Be precise and include all numerical data you can see."""
                        }
                    ]
                }
            ],
            max_tokens=1024
        )

        description = response.choices[0].message.content

    except Exception as e:
        # Return error message if API call fails
        description = f"Could not process image: {str(e)}"

    return {
        "content": description,
        "type": "image_description",
        "source": source
    }


def describe_all_images(images: list) -> list:
    """
    Describe all images from documents
    Processes each image through LLaVA vision model
    Returns list of description dicts
    """
    descriptions = []

    for i, img_data in enumerate(images):
        print(f"  Describing image {i+1}/{len(images)}...")

        description = describe_image(
            img_data["image"],
            img_data.get("source", "")
        )
        descriptions.append(description)

    return descriptions
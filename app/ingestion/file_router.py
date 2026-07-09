import os
from app.config.settings import ALLOWED_EXTENSIONS


def get_file_type(file_path: str) -> str:
    """
    Detect file type based on file extension
    Returns: 'pdf', 'docx', 'pptx', 'image', or 'unsupported'
    """
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return "pdf"
    elif extension == ".docx":
        return "docx"
    elif extension == ".pptx":
        return "pptx"
    elif extension in [".jpg", ".jpeg", ".png"]:
        return "image"
    else:
        return "unsupported"


def route_file(file_path: str) -> dict:
    """
    Route file to correct parser based on file type
    Returns file info dict with status, path, name and type
    """
    file_type = get_file_type(file_path)
    file_name = os.path.basename(file_path)

    # Return error for unsupported files
    if file_type == "unsupported":
        return {
            "status": "error",
            "message": f"{file_name} is not supported!",
            "file_type": None
        }

    return {
        "status": "success",
        "file_path": file_path,
        "file_name": file_name,
        "file_type": file_type
    }


def get_all_files(folder_path: str) -> list:
    """
    Get all supported files from a folder
    Returns list of file info dicts
    """
    all_files = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Process only files, skip directories
        if os.path.isfile(file_path):
            result = route_file(file_path)
            if result["status"] == "success":
                all_files.append(result)

    return all_files
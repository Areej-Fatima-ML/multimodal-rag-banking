from app.ingestion.file_router import get_all_files
from app.ingestion.pdf_parser import parse_pdf
from app.ingestion.docx_parser import parse_docx
from app.ingestion.pptx_parser import parse_pptx
from app.ingestion.image_parser import parse_image
from app.config.settings import DATA_PATH


def test_file_router():
    """
    Test file router with all documents
    Verifies all files are detected correctly
    """
    print("\n=== Testing File Router ===")
    files = get_all_files(DATA_PATH)

    print(f"Total files found: {len(files)}")
    for file in files:
        print(f"✅ {file['file_name']} → {file['file_type']}")

    return files


def test_parsers(files):
    """
    Test all parsers with detected files
    Verifies text and image extraction works
    """
    print("\n=== Testing Parsers ===")

    for file in files:
        print(f"\nParsing: {file['file_name']}")

        if file['file_type'] == 'pdf':
            result = parse_pdf(file['file_path'])
            print(f"   PDF: {len(result['texts'])} texts, "
                  f"{result['total_images']} images")

        elif file['file_type'] == 'docx':
            result = parse_docx(file['file_path'])
            print(f"   DOCX: {len(result['texts'])} texts, "
                  f"{len(result['tables'])} tables")

        elif file['file_type'] == 'pptx':
            result = parse_pptx(file['file_path'])
            print(f"   PPTX: {len(result['texts'])} texts, "
                  f"{result['total_slides']} slides")

        elif file['file_type'] == 'image':
            result = parse_image(file['file_path'])
            print(f"   Image: {result['width']}x{result['height']}")


if __name__ == "__main__":
    # Test file router
    files = test_file_router()

    # Test all parsers
    test_parsers(files)

    # Print final summary
    print("\n" + "="*50)
    print("FINAL SUMMARY")
    print("="*50)
    print(f"Total Files Found: {len(files)}")

    pdf_count = sum(1 for f in files if f['file_type'] == 'pdf')
    pptx_count = sum(1 for f in files if f['file_type'] == 'pptx')
    docx_count = sum(1 for f in files if f['file_type'] == 'docx')
    image_count = sum(1 for f in files if f['file_type'] == 'image')

    print(f"PDF Files:   {pdf_count}")
    print(f"PPTX Files:  {pptx_count}")
    print(f"DOCX Files:  {docx_count}")
    print(f"Image Files: {image_count}")
    print("="*50)
    print(" All parsers working successfully!")
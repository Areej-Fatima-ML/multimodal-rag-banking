import fitz  # PyMuPDF for PDF table extraction
import pandas as pd


def extract_tables_from_pdf(file_path: str) -> list:
    """
    Extract all tables from PDF file using PyMuPDF
    Converts tables to readable text format using pandas
    Returns list of table dicts with content and metadata
    """
    tables = []
    doc = fitz.open(file_path)

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Find all tables on this page
        page_tables = page.find_tables()

        for table_index, table in enumerate(page_tables):
            try:
                # Convert table to pandas dataframe
                df = table.to_pandas()

                # Convert dataframe to readable text
                table_text = df.to_string(index=False)

                # Only add non-empty tables
                if table_text.strip():
                    tables.append({
                        "content": table_text,
                        "page": page_num + 1,
                        "table_index": table_index,
                        "type": "table",
                        "source": file_path
                    })

            except Exception as e:
                # Skip tables that cannot be parsed
                print(f"Could not parse table on page {page_num + 1}: {e}")
                continue

    doc.close()
    return tables


def format_table_as_text(table_data: list) -> str:
    """
    Format table rows as clean readable text
    Joins cells with pipe separator
    Returns formatted string
    """
    if not table_data:
        return ""

    text_lines = []
    for row in table_data:
        row_text = " | ".join([str(cell) for cell in row if cell])
        if row_text.strip():
            text_lines.append(row_text)

    return "\n".join(text_lines)
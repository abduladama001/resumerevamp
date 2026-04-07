"""
extractor.py
------------
Handles reading and extracting plain text from uploaded PDF resume files.
Uses PyMuPDF (fitz) to parse each page and return all text as a single string.
"""

import fitz  # PyMuPDF


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract all text content from a PDF file.

    Args:
        uploaded_file: A file-like object from Streamlit's file_uploader.

    Returns:
        A single string containing all text extracted from the PDF.

    Raises:
        ValueError: If the file is empty or no text could be extracted.
    """
    text = ""

    try:
        # Read file bytes and open with PyMuPDF
        file_bytes = uploaded_file.read()
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        raise ValueError(f"Could not read the PDF file. Make sure it is a valid PDF.\nDetails: {e}")

    if not text.strip():
        raise ValueError(
            "No text could be extracted from this PDF. "
            "It may be a scanned image-based PDF. Please use a text-based PDF."
        )

    return text.strip()

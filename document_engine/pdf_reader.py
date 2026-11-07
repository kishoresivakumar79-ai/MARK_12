"""
PDF Reader for MARK 12
"""
from document_engine.text_extractor import PDFReader

def read_pdf(file_path: str) -> str:
    return PDFReader.extract_pdf(file_path)

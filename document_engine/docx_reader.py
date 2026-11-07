"""
DOCX Reader for MARK 12
"""
from document_engine.text_extractor import DocxReader

def read_docx(file_path: str) -> str:
    return DocxReader.extract_docx(file_path)

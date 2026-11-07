"""
Document readers and text extraction for MARK 12
Parses TXT, Markdown, PDF, and DOCX files.
"""
import os
from pathlib import Path
from typing import Optional

class TextExtractor:
    @staticmethod
    def extract_text(file_path: str) -> str:
        path = Path(file_path)
        if not path.exists():
            return ""
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            return f"Error reading text file: {e}"

class PDFReader:
    @staticmethod
    def extract_pdf(file_path: str) -> str:
        if not os.path.exists(file_path):
            return ""

        # 1. Try PyMuPDF (fitz)
        try:
            import fitz
            doc = fitz.open(file_path)
            pages = []
            for page in doc:
                pages.append(page.get_text())
            return "\n".join(pages)
        except Exception:
            pass

        # 2. Try pypdf
        try:
            import pypdf
            reader = pypdf.PdfReader(file_path)
            pages = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(pages)
        except Exception:
            pass

        return f"[PDF document: {os.path.basename(file_path)} parsed]"

class DocxReader:
    @staticmethod
    def extract_docx(file_path: str) -> str:
        if not os.path.exists(file_path):
            return ""

        try:
            import docx
            doc = docx.Document(file_path)
            paragraphs = [p.text for p in doc.paragraphs if p.text]
            return "\n".join(paragraphs)
        except Exception:
            pass

        return f"[DOCX document: {os.path.basename(file_path)} parsed]"

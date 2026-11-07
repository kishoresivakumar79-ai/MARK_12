"""
Universal Document Loader for MARK 12
Dispatches files to TXT, PDF, or DOCX extractors and produces semantic chunks.
"""
import os
from pathlib import Path
from typing import Dict, Any, List
from document_engine.text_extractor import TextExtractor, PDFReader, DocxReader
from document_engine.document_chunker import global_document_chunker

class DocumentLoader:
    def load_document(self, file_path: str) -> Dict[str, Any]:
        path = Path(file_path)
        ext = path.suffix.lower()
        content = ""

        if ext in [".txt", ".md", ".log", ".py", ".json", ".csv"]:
            content = TextExtractor.extract_text(file_path)
        elif ext == ".pdf":
            content = PDFReader.extract_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            content = DocxReader.extract_docx(file_path)
        else:
            content = TextExtractor.extract_text(file_path)

        chunks = global_document_chunker.chunk_text(content, source_doc=path.name)
        return {
            "file_name": path.name,
            "file_path": str(path),
            "file_type": ext,
            "full_text": content,
            "char_count": len(content),
            "chunks": chunks,
            "chunk_count": len(chunks)
        }

global_document_loader = DocumentLoader()

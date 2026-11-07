"""
Document and Files API Endpoint for MARK 12
POST /api/files/upload - Upload and chunk document
POST /api/files/qa - Ask questions grounded in loaded documents
"""
import os
import shutil
from pathlib import Path
from typing import Dict, Any, List
from document_engine.document_loader import global_document_loader
from document_engine.document_qa import global_document_qa
from database.connection import get_db

DOCS_DIR = Path("storage/documents")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# In-memory document chunk store for rapid QA
LOADED_DOCUMENTS: Dict[str, Dict[str, Any]] = {}

def process_file_upload(file_name: str, file_bytes: bytes) -> Dict[str, Any]:
    save_path = DOCS_DIR / file_name
    save_path.write_bytes(file_bytes)

    # Process through document loader
    parsed = global_document_loader.load_document(str(save_path))
    LOADED_DOCUMENTS[file_name] = parsed

    # Store in database
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO documents (id, filename, file_path, file_type, chunk_count, summary) VALUES (?, ?, ?, ?, ?, ?)",
            (file_name, file_name, str(save_path), parsed["file_type"], parsed["chunk_count"], parsed["full_text"][:200])
        )

    return {
        "file_name": file_name,
        "chunk_count": parsed["chunk_count"],
        "char_count": parsed["char_count"],
        "status": "indexed"
    }

def answer_doc_question(file_name: str, question: str) -> Dict[str, Any]:
    if file_name not in LOADED_DOCUMENTS:
        # Load from disk if exists
        target = DOCS_DIR / file_name
        if target.exists():
            LOADED_DOCUMENTS[file_name] = global_document_loader.load_document(str(target))
        else:
            return {"error": f"Document '{file_name}' not found."}

    chunks = LOADED_DOCUMENTS[file_name]["chunks"]
    return global_document_qa.answer_question(question, chunks)

try:
    from fastapi import APIRouter, UploadFile, File, Form
    router = APIRouter(prefix="/api/files", tags=["Files"])

    @router.post("/upload")
    async def upload_file_endpoint(file: UploadFile = File(...)):
        content = await file.read()
        return process_file_upload(file.filename, content)

    @router.post("/qa")
    async def doc_qa_endpoint(file_name: str = Form(...), question: str = Form(...)):
        return answer_doc_question(file_name, question)

    @router.get("")
    async def list_files_endpoint():
        files = []
        for p in DOCS_DIR.iterdir():
            if p.is_file() and not p.name.startswith("."):
                files.append({"filename": p.name, "size_bytes": p.stat().st_size})
        return files
except ImportError:
    router = None

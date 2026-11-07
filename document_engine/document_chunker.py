"""
Document Chunker for MARK 12
Splits raw text into overlapping semantic passages for RAG retrieval.
"""
from typing import List, Dict, Any

class DocumentChunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, source_doc: str = "") -> List[Dict[str, Any]]:
        words = text.split()
        if not words:
            return []

        chunks = []
        start = 0
        chunk_idx = 0

        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk_content = " ".join(words[start:end])
            chunks.append({
                "chunk_id": f"{source_doc}_chunk_{chunk_idx}",
                "source": source_doc,
                "index": chunk_idx,
                "text": chunk_content,
                "word_count": len(words[start:end])
            })
            chunk_idx += 1
            if end == len(words):
                break
            start += (self.chunk_size - self.overlap)

        return chunks

global_document_chunker = DocumentChunker()

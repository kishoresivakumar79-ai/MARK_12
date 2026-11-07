"""
Vector Memory Engine for MARK 12
Implements Vector Data Structure for semantic similarity retrieval.
Integrates with ChromaDB when available, with a resilient native vector fallback.
"""
from typing import List, Dict, Any, Optional
from ai_engine.embeddings.embedding_manager import global_embedding_manager
from database.connection import DB_DIR

class VectorMemory:
    def __init__(self):
        self.chroma_client = None
        self.collection = None
        self._in_memory_vectors: Dict[str, Dict[str, Any]] = {}
        self._init_backend()

    def _init_backend(self):
        try:
            import chromadb
            persist_path = str(DB_DIR / "chroma_db")
            self.chroma_client = chromadb.PersistentClient(path=persist_path)
            self.collection = self.chroma_client.get_or_create_collection(name="jarvis_memories")
        except Exception:
            # Fallback to internal high-performance vector store
            self.chroma_client = None
            self.collection = None

    def add_vector(self, item_id: str, text: str, metadata: Optional[Dict[str, Any]] = None):
        vec = global_embedding_manager.get_embedding(text)
        meta = metadata or {}
        
        if self.collection:
            try:
                self.collection.upsert(
                    ids=[item_id],
                    embeddings=[vec],
                    documents=[text],
                    metadatas=[meta]
                )
                return
            except Exception:
                pass

        # Native vector store
        self._in_memory_vectors[item_id] = {
            "id": item_id,
            "text": text,
            "vector": vec,
            "metadata": meta
        }

    def search_similar(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        query_vec = global_embedding_manager.get_embedding(query)
        results = []

        if self.collection:
            try:
                chroma_res = self.collection.query(
                    query_embeddings=[query_vec],
                    n_results=top_k
                )
                if chroma_res and "ids" in chroma_res and chroma_res["ids"]:
                    for i, doc_id in enumerate(chroma_res["ids"][0]):
                        results.append({
                            "id": doc_id,
                            "text": chroma_res["documents"][0][i],
                            "metadata": chroma_res["metadatas"][0][i] if "metadatas" in chroma_res else {},
                            "score": 1.0 - (chroma_res["distances"][0][i] if "distances" in chroma_res else 0.0)
                        })
                    return results
            except Exception:
                pass

        # Compute cosine similarity across native vector store
        scored = []
        for item_id, item in self._in_memory_vectors.items():
            sim = global_embedding_manager.cosine_similarity(query_vec, item["vector"])
            scored.append({
                "id": item_id,
                "text": item["text"],
                "metadata": item["metadata"],
                "score": sim
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def delete_vector(self, item_id: str):
        if self.collection:
            try:
                self.collection.delete(ids=[item_id])
            except Exception:
                pass
        self._in_memory_vectors.pop(item_id, None)

global_vector_memory = VectorMemory()

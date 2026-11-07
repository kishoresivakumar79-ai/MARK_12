"""
Document QA Engine for MARK 12
Performs semantic context retrieval and grounded question answering across uploaded documents.
"""
from typing import Dict, Any, List
from ai_engine.embeddings.embedding_manager import global_embedding_manager
from ai_engine.llm.model_manager import global_model_manager

class DocumentQA:
    def answer_question(self, question: str, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not chunks:
            return {
                "answer": "No document content provided to answer from.",
                "sources": []
            }

        q_vec = global_embedding_manager.get_embedding(question)
        scored_chunks = []

        for c in chunks:
            c_vec = global_embedding_manager.get_embedding(c["text"])
            score = global_embedding_manager.cosine_similarity(q_vec, c_vec)
            scored_chunks.append({
                "chunk": c,
                "score": score
            })

        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        top_chunks = scored_chunks[:3]

        context_str = "\n\n".join([f"[Passage {i+1}]: {item['chunk']['text']}" for i, item in enumerate(top_chunks)])

        prompt = (
            f"You are the Document Intelligence Specialist of MARK 12.\n"
            f"Answer the user's question accurately using ONLY the context provided below.\n\n"
            f"Context:\n{context_str}\n\n"
            f"User Question: {question}\n\n"
            f"Answer concisely with citations to the relevant passages."
        )

        answer = global_model_manager.generate_response(prompt)
        return {
            "answer": answer,
            "sources": [item["chunk"]["source"] for item in top_chunks]
        }

global_document_qa = DocumentQA()

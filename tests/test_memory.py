"""
Memory Unit Tests for MARK 12
Validates Short-Term, Long-Term, and Vector semantic similarity search.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from ai_engine.memory.short_term import global_short_term_memory
from ai_engine.memory.long_term import global_long_term_memory
from ai_engine.embeddings.embedding_manager import global_embedding_manager
from ai_engine.memory.vector_memory import global_vector_memory

def test_short_term_memory():
    global_short_term_memory.clear()
    global_short_term_memory.add("user", "Hello Jarvis")
    global_short_term_memory.add("assistant", "Greetings sir")
    window = global_short_term_memory.get_context_window()
    assert len(window) == 2
    assert window[0]["content"] == "Hello Jarvis"
    print("[PASS] test_short_term_memory")

def test_vector_similarity():
    vec1 = global_embedding_manager.get_embedding("Python programming language")
    vec2 = global_embedding_manager.get_embedding("Python coding script")
    vec3 = global_embedding_manager.get_embedding("Cooking chocolate cake recipe")

    sim_related = global_embedding_manager.cosine_similarity(vec1, vec2)
    sim_unrelated = global_embedding_manager.cosine_similarity(vec1, vec3)

    assert sim_related > sim_unrelated, f"Expected {sim_related} > {sim_unrelated}"
    print(f"[PASS] test_vector_similarity: related ({sim_related:.3f}) > unrelated ({sim_unrelated:.3f})")

def test_long_term_memory_recall():
    fact = "User's favorite programming language is Rust"
    mem_id = global_long_term_memory.remember(fact, category="user_fact", importance=5)
    assert mem_id is not None

    recalled = global_long_term_memory.recall("What is user's favorite language?")
    assert len(recalled) > 0
    # Clean up
    global_long_term_memory.forget(mem_id)
    print("[PASS] test_long_term_memory_recall")

if __name__ == "__main__":
    test_short_term_memory()
    test_vector_similarity()
    test_long_term_memory_recall()

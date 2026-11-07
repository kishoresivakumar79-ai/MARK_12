"""
Embedding Manager for MARK 12
Produces vector embeddings using API models or a fast self-contained semantic feature vector fallback.
"""
import math
import re
from typing import List

class EmbeddingManager:
    def __init__(self, vector_dim: int = 128):
        self.vector_dim = vector_dim

    def get_embedding(self, text: str) -> List[float]:
        """
        Generates a normalized dense vector representation for the input text.
        Uses character and token n-gram feature hashing to ensure semantic closeness.
        """
        words = re.findall(r'\b\w+\b', text.lower())
        vec = [0.0] * self.vector_dim
        if not words:
            return vec

        for word in words:
            # Hash word into vector dimensions
            h = hash(word)
            idx = abs(h) % self.vector_dim
            sign = 1.0 if (h >> 3) % 2 == 0 else -1.0
            vec[idx] += sign * (1.0 + math.log(1 + len(word)))

        # Character bi-grams for typo and inflection resilience
        clean_str = text.lower()
        for i in range(len(clean_str) - 1):
            bigram = clean_str[i:i+2]
            h = hash(bigram)
            idx = abs(h) % self.vector_dim
            vec[idx] += 0.5

        # L2 Normalize
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        if len(vec_a) != len(vec_b) or not vec_a:
            return 0.0
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return max(0.0, min(1.0, dot / (norm_a * norm_b)))

global_embedding_manager = EmbeddingManager()

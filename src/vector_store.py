"""
vector_store.py
===============
STEP 3 of the AI pipeline: store embeddings and search them fast.

This is a mini "vector database". When the user asks a question, we embed the
question and then ask this store: "which of my stored chunks are closest in
meaning?" It returns the top matches almost instantly, even with thousands of
chunks, thanks to FAISS (a free library made by Meta AI).
"""

from __future__ import annotations
from typing import List, Tuple
import numpy as np


class VectorStore:
    """Keeps text chunks together with their embeddings and finds the best matches."""

    def __init__(self, embedding_dim: int) -> None:
        import faiss  # free, fast similarity-search library

        # IndexFlatIP = Inner Product index. Because our vectors are normalized,
        # inner product == cosine similarity (higher score = more similar).
        self.index = faiss.IndexFlatIP(embedding_dim)
        self.chunks: List[str] = []  # the original text, kept in the same order

    def add(self, chunks: List[str], embeddings: np.ndarray) -> None:
        """Add a batch of text chunks and their embeddings to the store."""
        if len(chunks) == 0:
            return
        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def search(self, query_embedding: np.ndarray, top_k: int = 4) -> List[Tuple[str, float]]:
        """Return the `top_k` chunks most similar to the query.

        Parameters
        ----------
        query_embedding : np.ndarray
            The embedding of the user's question (1D vector).
        top_k : int
            How many chunks to return.

        Returns
        -------
        List of (chunk_text, similarity_score) tuples, best match first.
        """
        if self.index.ntotal == 0:
            return []

        # FAISS expects a 2D array, so we wrap the single vector.
        query = np.array([query_embedding], dtype="float32")
        scores, indices = self.index.search(query, min(top_k, self.index.ntotal))

        results: List[Tuple[str, float]] = []
        for idx, score in zip(indices[0], scores[0]):
            if idx == -1:  # FAISS uses -1 when there are fewer results than top_k
                continue
            results.append((self.chunks[idx], float(score)))
        return results

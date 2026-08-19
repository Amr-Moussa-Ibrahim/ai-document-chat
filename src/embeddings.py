"""
embeddings.py
=============
STEP 2 of the AI pipeline: turn text into "embeddings".

WHAT IS AN EMBEDDING? It's a list of numbers (a vector) that captures the
*meaning* of a piece of text. Two sentences that mean similar things get
similar numbers, even if they use different words. This is what lets the app
find the right paragraph to answer a question.

We use `sentence-transformers`, a free, open-source library. The default model
`all-MiniLM-L6-v2` is tiny (~90 MB), fast on a normal laptop CPU, and needs no
API key. It downloads automatically the first time you run the app.
"""

from __future__ import annotations
from typing import List
import numpy as np


class Embedder:
    """A thin, friendly wrapper around a free sentence-transformers model."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        # Import here so the heavy library only loads when actually needed.
        from sentence_transformers import SentenceTransformer

        # This line downloads the model the first time, then caches it locally.
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> np.ndarray:
        """Convert a list of texts into a 2D numpy array of embeddings.

        Returns an array of shape (number_of_texts, embedding_size).
        We normalize the vectors so that comparing them with a dot product
        equals cosine similarity (the standard way to measure "closeness").
        """
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,   # makes similarity search accurate
            show_progress_bar=False,
        )
        return embeddings.astype("float32")

    def embed_one(self, text: str) -> np.ndarray:
        """Embed a single string and return a 1D vector."""
        return self.embed([text])[0]

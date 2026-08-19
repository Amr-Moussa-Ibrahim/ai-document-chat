"""
chatbot.py
==========
STEP 4 (the finale): put everything together = "RAG".

RAG stands for **Retrieval-Augmented Generation**. It's the technique behind
most modern "chat with your data" AI apps. It works in two moves:

    1. RETRIEVE: find the chunks of your document that are relevant to the
       question (using embeddings + the vector store).
    2. GENERATE: give those chunks + the question to a language model and ask
       it to write an answer using ONLY that information.

This dramatically reduces "hallucinations" (made-up answers) because the model
is grounded in your actual document.

The language model here is Google's free, open-source `flan-t5-base`. It runs on
a normal CPU and needs no API key. It downloads automatically on first use.
"""

from __future__ import annotations
from typing import List, Tuple

from .document_loader import load_and_chunk, split_into_chunks
from .embeddings import Embedder
from .vector_store import VectorStore


class DocumentChatbot:
    """A self-contained 'chat with your documents' assistant."""

    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        generator_model: str = "google/flan-t5-base",
    ) -> None:
        # The part that understands meaning (Steps 2 & 3).
        self.embedder = Embedder(embedding_model)
        self.store: VectorStore | None = None

        # The part that writes answers (Step 4). Loaded lazily to keep startup fast.
        self._generator_model_name = generator_model
        self._generator = None

    # ------------------------------------------------------------------ #
    # Building the knowledge base
    # ------------------------------------------------------------------ #
    def add_file(self, file_path: str, chunk_size: int = 500, overlap: int = 100) -> int:
        """Load a file, chunk it, embed it, and add it to the searchable store.

        Returns the number of chunks that were added.
        """
        chunks = load_and_chunk(file_path, chunk_size=chunk_size, overlap=overlap)
        return self._index_chunks(chunks)

    def add_raw_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> int:
        """Same as add_file but for text you already have in memory."""
        chunks = split_into_chunks(text, chunk_size=chunk_size, overlap=overlap)
        return self._index_chunks(chunks)

    def _index_chunks(self, chunks: List[str]) -> int:
        if not chunks:
            return 0
        embeddings = self.embedder.embed(chunks)
        if self.store is None:
            self.store = VectorStore(embedding_dim=embeddings.shape[1])
        self.store.add(chunks, embeddings)
        return len(chunks)

    # ------------------------------------------------------------------ #
    # Answering questions
    # ------------------------------------------------------------------ #
    def _load_generator(self):
        """Load the text-generation model only the first time it's needed."""
        if self._generator is None:
            from transformers import pipeline

            # 'text2text-generation' is the right task type for flan-t5.
            self._generator = pipeline(
                "text2text-generation",
                model=self._generator_model_name,
            )
        return self._generator

    def ask(self, question: str, top_k: int = 4) -> Tuple[str, List[Tuple[str, float]]]:
        """Answer a question using the uploaded documents.

        Returns
        -------
        (answer, sources)
            answer  : the AI's written answer (str)
            sources : the chunks it used, as (text, score) tuples, so you can
                      show the user *where* the answer came from.
        """
        if self.store is None or self.store.index.ntotal == 0:
            return ("Please add a document first — I have nothing to read yet!", [])

        # 1. RETRIEVE the most relevant chunks.
        question_embedding = self.embedder.embed_one(question)
        sources = self.store.search(question_embedding, top_k=top_k)

        # 2. Build a clear prompt for the model.
        context = "\n\n".join(f"- {chunk}" for chunk, _score in sources)
        prompt = (
            "Answer the question using ONLY the context below. "
            "If the answer is not in the context, say you don't know.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n"
            "Answer:"
        )

        # 3. GENERATE the answer.
        generator = self._load_generator()
        output = generator(prompt, max_length=256, do_sample=False)
        answer = output[0]["generated_text"].strip()

        return answer, sources

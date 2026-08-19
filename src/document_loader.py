"""
document_loader.py
==================
STEP 1 of the AI pipeline: read a document and cut it into small "chunks".

WHY chunks? An AI model can only look at a limited amount of text at once.
So instead of feeding it a whole 100-page PDF, we break the text into small
overlapping pieces (e.g. ~500 characters each). Later we only send the AI the
few chunks that are actually relevant to the user's question.

Everything here is plain Python + one free library (pypdf) for reading PDFs.
"""

from __future__ import annotations
from pathlib import Path
from typing import List


def read_text_from_file(file_path: str) -> str:
    """Read raw text from a .txt, .md or .pdf file and return it as one string.

    Parameters
    ----------
    file_path : str
        Path to the file on disk.

    Returns
    -------
    str
        All the text found in the file.
    """
    path = Path(file_path)
    suffix = path.suffix.lower()

    # --- Plain text / markdown files ------------------------------------
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="ignore")

    # --- PDF files ------------------------------------------------------
    if suffix == ".pdf":
        # pypdf is a free library that extracts text from PDFs.
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    raise ValueError(
        f"Unsupported file type '{suffix}'. Please use .txt, .md or .pdf files."
    )


def split_into_chunks(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100,
) -> List[str]:
    """Cut a long string into smaller overlapping chunks.

    The "overlap" means each chunk repeats the last few words of the previous
    one. This keeps sentences that fall on a boundary from being split in a way
    that loses meaning.

    Parameters
    ----------
    text : str
        The full document text.
    chunk_size : int
        Roughly how many characters each chunk should contain.
    overlap : int
        How many characters to repeat between consecutive chunks.

    Returns
    -------
    List[str]
        A list of text chunks.
    """
    # Clean up whitespace so chunks are tidy.
    words = text.split()
    if not words:
        return []

    chunks: List[str] = []
    current: List[str] = []
    current_len = 0

    for word in words:
        current.append(word)
        current_len += len(word) + 1  # +1 for the space

        if current_len >= chunk_size:
            chunks.append(" ".join(current))
            # Start the next chunk with the last few words (the overlap).
            overlap_words: List[str] = []
            overlap_len = 0
            for w in reversed(current):
                overlap_len += len(w) + 1
                overlap_words.insert(0, w)
                if overlap_len >= overlap:
                    break
            current = overlap_words
            current_len = overlap_len

    # Don't forget the final, shorter chunk.
    if current:
        chunks.append(" ".join(current))

    return chunks


def load_and_chunk(file_path: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """Convenience helper: read a file AND split it into chunks in one call."""
    raw_text = read_text_from_file(file_path)
    return split_into_chunks(raw_text, chunk_size=chunk_size, overlap=overlap)

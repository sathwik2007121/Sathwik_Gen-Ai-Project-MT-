"""
ingest.py — PDF ingestion pipeline for the University RAG system.

Workflow:
  1. Load PDF page-by-page using PyMuPDF (fitz).
  2. Chunk each page with RecursiveCharacterTextSplitter-style logic.
  3. Embed chunks using sentence-transformers "all-MiniLM-L6-v2" (local, free).
  4. Store in ChromaDB with cosine distance; skip if already populated.

Usage:
    python ingest.py
"""

from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path
from typing import List, Tuple

import fitz  # PyMuPDF
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# ─── Configuration ────────────────────────────────────────────────────────────
PDF_PATH: str = "./mirai_academic_and_hostel_handbook_50p.pdf"
CHROMA_PATH: str = "./chroma_db"
COLLECTION_NAME: str = "university_policy"
EMBED_MODEL: str = "all-MiniLM-L6-v2"

CHUNK_SIZE: int = 800       # characters per chunk
CHUNK_OVERLAP: int = 150    # overlap to preserve context across boundaries

# Separators tried in order (most coarse → most fine-grained)
SEPARATORS: List[str] = ["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""]


# ─── Text Splitting ────────────────────────────────────────────────────────────

def _split_text(text: str, chunk_size: int, overlap: int, separators: List[str]) -> List[str]:
    """
    Recursively split `text` into chunks of at most `chunk_size` characters
    with `overlap` carry-over, trying each separator in order.

    This mirrors LangChain's RecursiveCharacterTextSplitter logic without the
    extra dependency on the full LangChain package.
    """
    if len(text) <= chunk_size:
        stripped = text.strip()
        return [stripped] if stripped else []

    # Try separators in order
    for sep in separators:
        if sep == "":
            # Last resort: hard-cut at chunk_size
            chunks: List[str] = []
            start = 0
            while start < len(text):
                end = start + chunk_size
                chunk = text[start:end].strip()
                if chunk:
                    chunks.append(chunk)
                start += chunk_size - overlap
            return chunks

        if sep in text:
            parts = text.split(sep)
            chunks: List[str] = []
            current = ""
            for part in parts:
                candidate = (current + sep + part) if current else part
                if len(candidate) <= chunk_size:
                    current = candidate
                else:
                    if current.strip():
                        chunks.append(current.strip())
                    # Carry overlap forward
                    words = current.split()
                    # Build overlap text from end of previous chunk
                    overlap_text = ""
                    for w in reversed(words):
                        trial = w + " " + overlap_text
                        if len(trial) <= overlap:
                            overlap_text = trial
                        else:
                            break
                    overlap_text = overlap_text.strip()
                    current = (overlap_text + sep + part).strip() if overlap_text else part
            if current.strip():
                chunks.append(current.strip())
            if chunks:
                return chunks

    return [text.strip()]


def chunk_page(text: str, page_num: int) -> List[Tuple[str, dict]]:
    """
    Chunk a single page of text. Returns list of (chunk_text, metadata) pairs.
    Metadata contains: page (1-indexed), chunk_id.
    """
    # Normalize whitespace: collapse 3+ blank lines to 2, strip trailing spaces
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    if not text:
        return []

    raw_chunks = _split_text(text, CHUNK_SIZE, CHUNK_OVERLAP, SEPARATORS)
    result: List[Tuple[str, dict]] = []
    for idx, chunk in enumerate(raw_chunks):
        if not chunk.strip():
            continue
        chunk_id = f"p{page_num}_c{idx}"
        result.append((chunk, {"page": page_num, "chunk_id": chunk_id}))
    return result


# ─── PDF Loading ───────────────────────────────────────────────────────────────

def load_pdf(pdf_path: str) -> List[Tuple[int, str]]:
    """
    Load a PDF and return a list of (page_number, page_text) tuples.
    Page numbers are 1-indexed. Uses PyMuPDF for robust extraction.
    """
    path = Path(pdf_path)
    if not path.exists():
        print(f"[ERROR] PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    doc = fitz.open(str(path))
    pages: List[Tuple[int, str]] = []
    for i, page in enumerate(doc, start=1):
        # get_text("text") preserves layout reasonably; "blocks" can help too
        text = page.get_text("text")
        pages.append((i, text))
    doc.close()
    print(f"[ingest] Loaded {len(pages)} pages from '{pdf_path}'")
    return pages


# ─── Embedding & ChromaDB ──────────────────────────────────────────────────────

def get_collection(client: chromadb.PersistentClient) -> chromadb.Collection:
    """Get or create the ChromaDB collection with cosine distance."""
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def embed_and_store(
    chunks: List[Tuple[str, dict]],
    model: SentenceTransformer,
    collection: chromadb.Collection,
    batch_size: int = 64,
) -> None:
    """
    Encode chunks and upsert into ChromaDB in batches.
    """
    texts = [c[0] for c in chunks]
    metadatas = [c[1] for c in chunks]
    ids = [m["chunk_id"] for m in metadatas]

    total = len(texts)
    print(f"[ingest] Embedding {total} chunks in batches of {batch_size}...")
    t0 = time.time()

    for start in range(0, total, batch_size):
        batch_texts = texts[start : start + batch_size]
        batch_meta = metadatas[start : start + batch_size]
        batch_ids = ids[start : start + batch_size]

        embeddings = model.encode(batch_texts, normalize_embeddings=True).tolist()

        collection.upsert(
            ids=batch_ids,
            documents=batch_texts,
            embeddings=embeddings,
            metadatas=batch_meta,
        )
        print(f"  → batch {start // batch_size + 1}: stored {len(batch_texts)} chunks")

    elapsed = time.time() - t0
    print(f"[ingest] Done. Total embedding time: {elapsed:.1f}s")


# ─── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 60)
    print("University RAG — Ingestion Pipeline")
    print("=" * 60)

    # 1. Connect to ChromaDB (persistent)
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = get_collection(client)

    existing_count = collection.count()
    if existing_count > 0:
        print(
            f"[ingest] Collection '{COLLECTION_NAME}' already has {existing_count} chunks. "
            "Skipping ingestion (persistence check passed)."
        )
        print("[ingest] If you want to re-ingest, delete ./chroma_db and re-run.")
        return

    # 2. Load PDF
    pages = load_pdf(PDF_PATH)

    # 3. Chunk all pages
    all_chunks: List[Tuple[str, dict]] = []
    for page_num, page_text in pages:
        page_chunks = chunk_page(page_text, page_num)
        all_chunks.extend(page_chunks)
    print(f"[ingest] Total chunks produced: {len(all_chunks)}")

    if not all_chunks:
        print("[ERROR] No chunks extracted. Check the PDF path and content.", file=sys.stderr)
        sys.exit(1)

    # 4. Load embedding model (downloads once, then cached)
    print(f"[ingest] Loading embedding model '{EMBED_MODEL}'...")
    model = SentenceTransformer(EMBED_MODEL)

    # 5. Embed and store
    embed_and_store(all_chunks, model, collection)

    # 6. Confirm persistence
    final_count = collection.count()
    print(f"\n[ingest] ✓ Stored {final_count} chunks in ChromaDB at '{CHROMA_PATH}'")
    print(f"[ingest] ✓ Pages: {len(pages)}, Chunks: {final_count}")
    print("[ingest] ✓ Persistence confirmed — ChromaDB is ready for queries.")


if __name__ == "__main__":
    main()

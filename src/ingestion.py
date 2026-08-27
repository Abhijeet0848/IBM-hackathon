"""
Document Ingestion & Local Vector Database Management (ChromaDB)
Extracts, chunks, embeds, and stores syllabus/notes locally with ultra-fast local embeddings.
"""

import os
import io
import re
import math
from typing import List, Dict, Any, Optional
import pypdf

# Standalone robust recursive character & line-aware text splitter
class FastTextSplitter:
    def __init__(self, chunk_size=800, chunk_overlap=100, separators=None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

    def split_text(self, text: str) -> List[str]:
        if not text:
            return []
        text = text.strip()
        if len(text) <= self.chunk_size:
            return [text]

        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            if text_len - start <= self.chunk_size:
                last_chunk = text[start:].strip()
                if last_chunk and len(last_chunk) >= 15 and (not chunks or last_chunk != chunks[-1]):
                    chunks.append(last_chunk)
                break
                
            end = start + self.chunk_size
            # Find best separator to break naturally
            split_pos = -1
            for sep in self.separators:
                pos = text.rfind(sep, start, end)
                if pos > start:
                    split_pos = pos + len(sep)
                    break
            
            if split_pos == -1 or split_pos <= start:
                split_pos = end

            chunk = text[start:split_pos].strip()
            if chunk and len(chunk) >= 15:
                if not chunks or chunk != chunks[-1]:
                    chunks.append(chunk)
            
            next_start = split_pos - self.chunk_overlap
            if next_start <= start:
                next_start = split_pos
            start = next_start

        return chunks if chunks else [text]

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings

class FastDenseEmbeddingFunction(EmbeddingFunction):
    """
    Zero-network, ultra-fast 128-dimensional dense semantic hashing embedding function.
    Guarantees instant local startup without downloading huge model weights.
    """
    def __init__(self, dim: int = 128):
        self.dim = dim

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            vec = [0.0] * self.dim
            words = re.findall(r'\w+', text.lower())
            if not words:
                embeddings.append(vec)
                continue
            for i, word in enumerate(words):
                h = hash(word) & 0xffffffff
                idx = h % self.dim
                sign = 1.0 if ((h >> 8) & 1) else -1.0
                vec[idx] += sign * (1.0 + math.log(1.0 + len(word)))

                # N-gram hashing for local semantic context
                if i < len(words) - 1:
                    bigram = word + "_" + words[i+1]
                    h_bi = hash(bigram) & 0xffffffff
                    idx_bi = h_bi % self.dim
                    vec[idx_bi] += 0.5

            norm = math.sqrt(sum(v * v for v in vec)) or 1.0
            norm_vec = [v / norm for v in vec]
            embeddings.append(norm_vec)
        return embeddings

class DocumentIngestionPipeline:
    def __init__(self, persist_directory: Optional[str] = None):
        """
        Initializes the document ingestion pipeline with ChromaDB.
        """
        self.persist_directory = persist_directory
        if persist_directory:
            os.makedirs(persist_directory, exist_ok=True)
            self.client = chromadb.PersistentClient(path=persist_directory)
        else:
            self.client = chromadb.Client()

        self.embedding_fn = FastDenseEmbeddingFunction(dim=128)
        self.collection_name = "study_materials_v2"
        self.collection = self._get_or_create_collection()
        self.text_splitter = FastTextSplitter(chunk_size=800, chunk_overlap=150)

    def _get_or_create_collection(self):
        """Fetches or creates the Chroma collection."""
        try:
            return self.client.get_or_create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_fn
            )
        except Exception:
            try:
                self.client.delete_collection(name=self.collection_name)
            except Exception:
                pass
            return self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_fn
            )

    def extract_text_from_file(self, file_obj: Any, filename: str) -> str:
        """Extracts raw text from PDF or Text file."""
        text = ""
        ext = filename.lower().split(".")[-1]

        if ext == "pdf":
            try:
                if isinstance(file_obj, (str, os.PathLike)):
                    reader = pypdf.PdfReader(file_obj)
                elif hasattr(file_obj, "read"):
                    if hasattr(file_obj, "seek"):
                        file_obj.seek(0)
                    reader = pypdf.PdfReader(io.BytesIO(file_obj.read()))
                else:
                    reader = pypdf.PdfReader(file_obj)

                for page_idx, page in enumerate(reader.pages):
                    extracted = page.extract_text()
                    if extracted:
                        text += f"\n--- Page {page_idx + 1} ---\n" + extracted
            except Exception as e:
                raise ValueError(f"Failed to extract text from PDF '{filename}': {str(e)}")

        elif ext in ["txt", "md", "csv", "json"]:
            try:
                if isinstance(file_obj, (str, os.PathLike)):
                    with open(file_obj, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                elif hasattr(file_obj, "read"):
                    if hasattr(file_obj, "seek"):
                        file_obj.seek(0)
                    raw = file_obj.read()
                    text = raw.decode("utf-8", errors="ignore") if isinstance(raw, bytes) else str(raw)
            except Exception as e:
                raise ValueError(f"Failed to read text file '{filename}': {str(e)}")
        else:
            raise ValueError(f"Unsupported file format '.{ext}'. Please upload a .pdf or .txt file.")

        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        return text.strip()

    def process_and_store(self, file_obj: Any, filename: str) -> Dict[str, Any]:
        """Processes and indexes chunks in ChromaDB."""
        raw_text = self.extract_text_from_file(file_obj, filename)
        if not raw_text:
            raise ValueError(f"No extractable text found in '{filename}'.")

        chunks = self.text_splitter.split_text(raw_text)
        if not chunks:
            raise ValueError("Document was empty or could not be chunked.")

        ids = [f"{filename}_chunk_{i}_{hash(chunk) & 0xffffffff:x}" for i, chunk in enumerate(chunks)]
        metadatas = [
            {
                "source": filename,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "char_length": len(chunk)
            }
            for i, chunk in enumerate(chunks)
        ]

        self.collection.add(
            ids=ids,
            documents=chunks,
            metadatas=metadatas
        )

        return {
            "filename": filename,
            "char_count": len(raw_text),
            "chunk_count": len(chunks),
            "total_items_in_db": self.collection.count()
        }

    def query_similarity(self, query_text: str, n_results: int = 4) -> List[Dict[str, Any]]:
        """Searches ChromaDB for top-k matching chunks."""
        count = self.collection.count()
        if count == 0:
            return []

        limit = min(n_results, count)
        results = self.collection.query(
            query_texts=[query_text],
            n_results=limit
        )

        formatted_chunks = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if "metadatas" in results and results["metadatas"] else [{}] * len(docs)
            dists = results["distances"][0] if "distances" in results and results["distances"] else [0.0] * len(docs)
            ids = results["ids"][0] if "ids" in results and results["ids"] else [""] * len(docs)

            for doc, meta, dist, chunk_id in zip(docs, metas, dists, ids):
                formatted_chunks.append({
                    "id": chunk_id,
                    "content": doc,
                    "metadata": meta,
                    "distance": dist
                })

        return formatted_chunks

    def get_all_chunks(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves all indexed chunks with their metadata."""
        count = self.collection.count()
        if count == 0:
            return []
        peek = self.collection.peek(limit=min(count, limit))
        formatted = []
        if peek and "documents" in peek and peek["documents"]:
            docs = peek["documents"]
            metas = peek["metadatas"] if "metadatas" in peek and peek["metadatas"] else [{}] * len(docs)
            ids = peek["ids"] if "ids" in peek and peek["ids"] else [""] * len(docs)
            for doc, meta, chunk_id in zip(docs, metas, ids):
                formatted.append({
                    "id": chunk_id,
                    "content": doc,
                    "metadata": meta,
                    "distance": 0.0
                })
        return formatted

    def reset_database(self) -> None:
        """Clears all stored documents."""
        try:
            self.client.delete_collection(name=self.collection_name)
        except Exception:
            pass
        self.collection = self.client.create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_fn
        )

    def get_stats(self) -> Dict[str, Any]:
        """Returns statistics about current stored materials."""
        count = self.collection.count()
        sources = set()
        if count > 0:
            try:
                peek = self.collection.peek(limit=count)
                if peek and "metadatas" in peek:
                    for meta in peek["metadatas"]:
                        if meta and "source" in meta:
                            sources.add(meta["source"])
            except Exception:
                pass
        return {
            "total_chunks": count,
            "unique_documents": list(sources),
            "document_count": len(sources)
        }

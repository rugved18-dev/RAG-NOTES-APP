"""Lightweight RAG chain using TF-IDF retrieval and optional Hugging Face
Inference API generation.

This implementation keeps retrieval local (very small footprint) and uses a
remote generator (Hugging Face Inference API) so you don't need to download
large models to your machine.

Usage:
  - Initialize with `RAGChain(backend='hf', hf_token='...')`
  - Call `add_documents(documents, filename)` where `documents` are
    `langchain.schema.Document`-like objects (they only need `page_content`
    and `.metadata`).
  - Call `query(question)` to retrieve and generate an answer.
"""
import os
from typing import Optional, List, Dict, Tuple
import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RAGChain:
    """Lightweight RAG chain.

    Retrieval: TF-IDF over document chunks.
    Generation (optional): Hugging Face Inference API (remote) — specify
    `backend='hf'` and provide `hf_token`.
    """

    def __init__(self, backend: str = "hf", hf_token: Optional[str] = None,
                 temperature: float = 0.7, hf_model: str = "google/flan-t5-small"):
        self.backend = backend
        self.hf_token = hf_token
        self.temperature = temperature
        self.hf_model = hf_model

        # In-memory document store
        self._doc_texts: List[str] = []
        self._metadata: List[Dict] = []

        # TF-IDF index
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix: Optional[np.ndarray] = None

        # Chat history
        self.chat_history: List[Dict] = []

    def set_temperature(self, temperature: float):
        self.temperature = temperature

    def add_documents(self, documents: List[object], file_name: str) -> str:
        """Add list of Document-like objects (must have .page_content and .metadata).

        Returns a string message on success.
        """
        added = 0
        for doc in documents:
            try:
                text = getattr(doc, "page_content", None)
                metadata = getattr(doc, "metadata", {})
                if not text:
                    continue
                self._doc_texts.append(text)
                md = dict(metadata)
                md.setdefault("source", file_name)
                self._metadata.append(md)
                added += 1
            except Exception:
                continue

        # Rebuild TF-IDF index
        if self._doc_texts:
            self.vectorizer = TfidfVectorizer(stop_words="english")
            self.tfidf_matrix = self.vectorizer.fit_transform(self._doc_texts)

        return f"Successfully added {added} chunks from {file_name}"

    def load_existing_store(self) -> bool:
        # No persistence in this lightweight implementation
        return False

    def _retrieve(self, query: str, k: int = 4) -> List[Tuple[int, float]]:
        """Retrieve top-k document indices with similarity scores.

        Returns list of (index, score).
        """
        if self.vectorizer is None or self.tfidf_matrix is None:
            return []

        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.tfidf_matrix).flatten()
        if np.all(np.isnan(sims)):
            return []
        idxs = np.argsort(-sims)[:k]
        return [(int(i), float(sims[i])) for i in idxs if sims[i] > 0]

    def _generate_with_hf(self, prompt: str) -> str:
        """Send prompt to Hugging Face Inference API and return text.

        Requires `self.hf_token` to be set.
        """
        if not self.hf_token:
            raise ValueError("Hugging Face token not provided (hf_token)")

        url = f"https://api-inference.huggingface.co/models/{self.hf_model}"
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 256, "temperature": self.temperature},
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        if resp.status_code != 200:
            raise Exception(f"HF Inference error {resp.status_code}: {resp.text}")

        data = resp.json()
        # HF may return a string or a dict/list depending on model; handle common shapes
        if isinstance(data, dict) and "error" in data:
            raise Exception(f"HF error: {data['error']}")
        if isinstance(data, list):
            # sequence of dicts with generated_text
            if isinstance(data[0], dict) and "generated_text" in data[0]:
                return data[0]["generated_text"]
            # some models return plain text in a list
            if isinstance(data[0], str):
                return data[0]
        if isinstance(data, str):
            return data

        # Fallback: stringify
        return str(data)

    def query(self, question: str) -> Dict:
        """Run retrieval + generation and return answer with sources."""
        if not self._doc_texts:
            return {"answer": "Please upload at least one document first.", "sources": []}

        hits = self._retrieve(question, k=4)
        if not hits:
            return {"answer": "No relevant content found in uploaded documents.", "sources": []}

        context_parts = []
        sources = []
        for idx, score in hits:
            context_parts.append(self._doc_texts[idx])
            md = self._metadata[idx] if idx < len(self._metadata) else {}
            sources.append({"file": md.get("source", "Unknown"), "meta": md, "score": score})

        context = "\n\n".join(context_parts)

        prompt = (
            "You are a helpful assistant. Use the context from the documents below to answer the question."
            " Always cite the source filename when referencing facts.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        )

        try:
            if self.backend == "hf":
                answer = self._generate_with_hf(prompt)
            else:
                # No local generator configured; return concatenated context as answer
                answer = (
                    "(No remote generator configured)\n" +
                    "Here is the collected context that may help answer your question:\n\n" + context
                )
        except Exception as e:
            return {"answer": f"Error generating answer: {str(e)}", "sources": sources}

        # Store in chat history
        self.chat_history.append({"question": question, "answer": answer, "sources": sources})

        return {"answer": answer, "sources": sources}

    def clear_memory(self):
        self.chat_history = []

    def get_collection_info(self) -> Dict:
        return {"status": "Documents loaded" if self._doc_texts else "No documents", "total_chunks": len(self._doc_texts)}
 
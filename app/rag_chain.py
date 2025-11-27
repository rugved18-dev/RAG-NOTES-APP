"""RAG Chain using OpenAI API and ChromaDB vector database."""
import os
from typing import Optional, List, Dict
import chromadb
from chromadb.config import Settings
from langchain.schema import Document
from openai import OpenAI, APIError


class RAGChain:
    """RAG chain using OpenAI and ChromaDB.
    
    Handles:
    - Document storage with ChromaDB vector database
    - Semantic search using OpenAI embeddings
    - Question answering with context using GPT-3.5-Turbo
    - Conversation memory for follow-up questions
    """

    def __init__(self, temperature: float = 0.7):
        self.temperature = temperature
        self.chat_history: List[Dict] = []
        
        # Initialize ChromaDB
        settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=".chroma",
            anonymized_telemetry=False,
            allow_reset=True,
        )
        self.client = chromadb.Client(settings)
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name="documents")
        except Exception:
            self.collection = self.client.create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
        
        # OpenAI client
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not set. Please set it in .env file or via the app sidebar."
            )
        self.openai_client = OpenAI(api_key=api_key)

    def set_temperature(self, temperature: float):
        """Set temperature for response generation."""
        self.temperature = temperature

    def add_documents(self, documents: List, file_name: str) -> str:
        """Add documents to the vector database.
        
        Args:
            documents: List of Document objects with page_content and metadata
            file_name: Source file name for tracking
            
        Returns:
            Success message with count of added documents
        """
        added = 0
        for i, doc in enumerate(documents):
            try:
                text = getattr(doc, "page_content", None)
                metadata = getattr(doc, "metadata", {})
                
                if not text or len(text.strip()) < 10:
                    continue
                
                # Prepare metadata with file info
                doc_metadata = dict(metadata)
                doc_metadata["source"] = file_name
                
                # Add to ChromaDB
                doc_id = f"{file_name}_{i}"
                self.collection.add(
                    ids=[doc_id],
                    documents=[text],
                    metadatas=[doc_metadata]
                )
                added += 1
                
            except Exception as e:
                print(f"Error adding document {i}: {str(e)}")
                continue
        
        return f"✅ Successfully added {added} chunks from {file_name}"

    def load_existing_store(self) -> bool:
        """Check if documents exist in the store."""
        try:
            count = self.collection.count()
            return count > 0
        except Exception:
            return False

    def _retrieve(self, query: str, k: int = 4) -> List[Dict]:
        """Retrieve relevant documents from ChromaDB.
        
        Args:
            query: User's question
            k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents with metadata
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=k,
                include=["documents", "metadatas", "distances"]
            )
            
            documents = []
            if results and len(results["documents"]) > 0:
                for i, doc in enumerate(results["documents"][0]):
                    metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                    distance = results["distances"][0][i] if results["distances"] else 0
                    
                    documents.append({
                        "content": doc,
                        "file": metadata.get("source", "Unknown"),
                        "page": metadata.get("page", "Unknown"),
                        "distance": distance
                    })
            
            return documents
            
        except Exception as e:
            print(f"Error retrieving documents: {str(e)}")
            return []

    def query(self, question: str) -> Dict:
        """Answer a question using retrieved context.
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with answer and sources
        """
        # Check if documents exist
        if not self.load_existing_store():
            return {
                "answer": "📚 Please upload documents first in the sidebar to start asking questions.",
                "sources": []
            }
        
        # Retrieve relevant documents
        retrieved_docs = self._retrieve(question, k=4)
        if not retrieved_docs:
            return {
                "answer": "❌ No relevant content found. Try asking a different question or upload more documents.",
                "sources": []
            }
        
        # Build context
        context = "\n\n".join([f"[{doc['file']} - Page {doc['page']}]\n{doc['content']}" 
                               for doc in retrieved_docs])
        
        # Build chat history for context (last 4 messages)
        history_context = ""
        if self.chat_history:
            history_context = "\n\nPrevious conversation:\n"
            for msg in self.chat_history[-4:]:
                history_context += f"Q: {msg['question']}\nA: {msg['answer'][:200]}...\n\n"
        
        # Create prompt
        prompt = f"""You are a helpful assistant that answers questions based on provided documents.

{history_context}

Context from documents:
{context}

Question: {question}

Instructions:
- Answer based only on the provided context
- Be accurate and cite sources when relevant
- If the answer spans multiple documents, mention each one
- Keep answers concise but thorough"""
        
        try:
            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful document assistant. Answer questions based only on provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=1000,
                top_p=0.9,
            )
            
            answer = response.choices[0].message.content.strip()
            
        except APIError as e:
            return {
                "answer": f"⚠️ API Error: {str(e)}. Please check your OpenAI API key.",
                "sources": []
            }
        except Exception as e:
            return {
                "answer": f"❌ Error: {str(e)}",
                "sources": []
            }
        
        # Prepare sources for display
        sources = [
            {
                "file": doc["file"],
                "page": doc["page"]
            }
            for doc in retrieved_docs
        ]
        
        # Store in chat history
        self.chat_history.append({
            "question": question,
            "answer": answer,
            "sources": sources
        })
        
        return {
            "answer": answer,
            "sources": sources
        }

    def clear_memory(self):
        """Clear chat history but keep documents."""
        self.chat_history = []

    def get_collection_info(self) -> Dict:
        """Get information about stored documents."""
        try:
            count = self.collection.count()
            return {
                "status": "✅ Ready" if count > 0 else "⏳ Empty",
                "total_chunks": count
            }
        except Exception as e:
            return {
                "status": f"❌ Error: {str(e)}",
                "total_chunks": 0
            }

 
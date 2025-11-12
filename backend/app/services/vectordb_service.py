"""
Vector Database Service
Handles ChromaDB operations for storing and retrieving embeddings
"""

import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict
from pathlib import Path


class VectorDBService:
    """Service for vector database operations"""
    
    def __init__(self, persist_directory: Path, embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize vector database service
        
        Args:
            persist_directory: Directory to persist the database
            embedding_model: Name of the sentence-transformers model to use
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(exist_ok=True, parents=True)
        
        print(f"📊 Initializing vector database...")
        print(f"   Persist directory: {self.persist_directory}")
        print(f"   Embedding model: {embedding_model}")
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))
        
        # Initialize embedding function
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )
        
        self.collection = None
    
    def create_collection(self, collection_name: str = "scirag_papers", reset: bool = False):
        """
        Create or get a collection
        
        Args:
            collection_name: Name of the collection
            reset: If True, delete existing collection and create new one
        """
        if reset:
            try:
                self.client.delete_collection(collection_name)
                print(f"   🗑️  Deleted existing collection: {collection_name}")
            except:
                pass
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )
        
        print(f"   ✅ Collection ready: {collection_name}")
        return self.collection
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict],
        ids: List[str]
    ):
        """
        Add documents to the collection
        
        Args:
            documents: List of text chunks to add
            metadatas: List of metadata dictionaries
            ids: List of unique IDs for each document
        """
        if not self.collection:
            raise ValueError("Collection not initialized. Call create_collection() first.")
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"   💾 Added {len(documents)} documents to vector database")
    
    def query(
        self,
        query_text: str,
        n_results: int = 5,
        where: Dict = None
    ) -> Dict:
        """
        Query the collection for similar documents
        
        Args:
            query_text: Query string
            n_results: Number of results to return
            where: Optional filter conditions
            
        Returns:
            Dictionary with query results
        """
        if not self.collection:
            raise ValueError("Collection not initialized. Call create_collection() first.")
        
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where
        )
        
        return results
    
    def get_collection_stats(self) -> Dict:
        """
        Get statistics about the collection
        
        Returns:
            Dictionary with collection statistics
        """
        if not self.collection:
            return {'count': 0, 'name': None}
        
        count = self.collection.count()
        return {
            'count': count,
            'name': self.collection.name
        }
    
    def clear_collection(self):
        """Delete all documents from the collection"""
        if self.collection:
            self.client.delete_collection(self.collection.name)
            self.collection = None
            print("   🗑️  Collection cleared")

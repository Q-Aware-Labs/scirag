"""
SciRAG Agent
Main orchestrator that coordinates all services
"""

import anthropic
from typing import List, Dict
from pathlib import Path

from ..services.arxiv_service import ArxivService
from ..services.pdf_service import PDFService
from ..services.vectordb_service import VectorDBService
from ..config import settings


class SciRAGAgent:
    """
    Main SciRAG Agent
    Orchestrates paper search, processing, and question answering
    """
    
    def __init__(
        self,
        anthropic_api_key: str = None,
        download_dir: Path = None,
        chroma_dir: Path = None
    ):
        """
        Initialize SciRAG Agent with all services
        
        Args:
            anthropic_api_key: Anthropic API key (uses settings if None)
            download_dir: Directory for downloaded PDFs (uses settings if None)
            chroma_dir: Directory for ChromaDB (uses settings if None)
        """
        print("🚀 Initializing SciRAG Agent...")
        
        # Initialize API key
        self.anthropic_api_key = anthropic_api_key or settings.ANTHROPIC_API_KEY
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")
        
        self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
        
        # Initialize services
        download_dir = download_dir or settings.DOWNLOAD_DIR
        chroma_dir = chroma_dir or settings.CHROMA_PERSIST_DIR
        
        self.arxiv_service = ArxivService(download_dir=download_dir)
        self.pdf_service = PDFService(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        self.vectordb_service = VectorDBService(
            persist_directory=chroma_dir,
            embedding_model=settings.EMBEDDING_MODEL
        )
        
        # Initialize collection
        self.vectordb_service.create_collection(reset=False)
        
        # Store paper metadata
        self.papers_metadata = {}
        
        print("✅ SciRAG Agent initialized successfully!\n")
    
    def search_papers(self, query: str, max_results: int = None) -> List:
        """
        Search arXiv for papers
        
        Args:
            query: Search query
            max_results: Maximum papers to return (uses settings if None)
            
        Returns:
            List of paper results
        """
        max_results = max_results or settings.MAX_PAPERS
        return self.arxiv_service.search_papers(query, max_results)
    
    def process_paper(self, paper) -> bool:
        """
        Process a single paper: download, extract, chunk, and index
        
        Args:
            paper: arXiv paper result
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\n📝 Processing: {paper.title[:60]}...")
        
        try:
            # Download PDF
            pdf_path = self.arxiv_service.download_pdf(paper)
            
            # Extract and chunk text
            result = self.pdf_service.process_pdf(pdf_path)
            
            if not result['success']:
                return False
            
            # Get metadata
            metadata = self.arxiv_service.get_paper_metadata(paper)
            paper_id = metadata['paper_id']
            
            # Store metadata
            self.papers_metadata[paper_id] = metadata
            
            # Prepare for vector DB
            chunks = result['chunks']
            ids = [f"{paper_id}_chunk_{i}" for i in range(len(chunks))]
            metadatas = [{
                'paper_id': paper_id,
                'title': paper.title,
                'chunk_index': i,
                'authors': ', '.join(metadata['authors'][:3])
            } for i in range(len(chunks))]
            
            # Add to vector database
            self.vectordb_service.add_documents(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"   ✅ Successfully processed paper!\n")
            return True
            
        except Exception as e:
            print(f"   ❌ Error processing paper: {e}\n")
            return False
    
    def process_papers(self, papers: List) -> Dict:
        """
        Process multiple papers
        
        Args:
            papers: List of arXiv paper results
            
        Returns:
            Dictionary with processing statistics
        """
        print("\n" + "="*70)
        print("                    📚 PROCESSING PAPERS")
        print("="*70)
        
        successful = 0
        failed = 0
        
        for paper in papers:
            if self.process_paper(paper):
                successful += 1
            else:
                failed += 1
        
        print(f"\n✅ Successfully processed {successful}/{len(papers)} papers")
        
        if failed > 0:
            print(f"⚠️  Failed to process {failed} paper(s)")
        
        return {
            'total': len(papers),
            'successful': successful,
            'failed': failed
        }
    
    def query(self, question: str, n_results: int = 5) -> Dict:
        """
        Answer a question using RAG
        
        Args:
            question: User's question
            n_results: Number of chunks to retrieve
            
        Returns:
            Dictionary with answer and sources
        """
        print("="*70)
        print(f"💬 USER QUERY: {question}")
        print("="*70 + "\n")
        
        # Retrieve relevant chunks
        print(f"🔎 Retrieving relevant content...")
        results = self.vectordb_service.query(question, n_results=n_results)
        
        if not results['documents'][0]:
            return {
                'answer': "I couldn't find any relevant information in the indexed papers.",
                'sources': [],
                'success': False
            }
        
        print(f"✅ Found {len(results['documents'][0])} relevant chunks\n")
        
        # Generate response
        answer = self._generate_response(
            question,
            results['documents'][0],
            results['metadatas'][0]
        )
        
        # Collect unique sources
        sources = []
        seen_papers = set()
        for meta in results['metadatas'][0]:
            paper_id = meta['paper_id']
            if paper_id not in seen_papers and paper_id in self.papers_metadata:
                sources.append(self.papers_metadata[paper_id])
                seen_papers.add(paper_id)
        
        return {
            'answer': answer,
            'sources': sources,
            'success': True
        }
    
    def _generate_response(
        self,
        query: str,
        context_chunks: List[str],
        metadata: List[Dict]
    ) -> str:
        """
        Generate response using Claude with RAG context
        
        Args:
            query: User's question
            context_chunks: Retrieved text chunks
            metadata: Metadata for each chunk
            
        Returns:
            Generated answer
        """
        print("🤖 Generating response with Claude...\n")
        
        # Build context from chunks
        context = "\n\n".join([
            f"[From: {meta['title']}]\n{chunk}"
            for chunk, meta in zip(context_chunks, metadata)
        ])
        
        # Create prompt
        prompt = f"""You are a helpful scientific research assistant. You have access to content from relevant research papers.

Based on the following excerpts from scientific papers, please answer the user's question. Be specific and cite which paper you're referencing when possible.

Research Paper Excerpts:
{context}

User Question: {query}

Please provide a clear, well-structured answer based on the papers above. If the papers don't contain enough information to fully answer the question, acknowledge this."""

        # Call Claude
        message = self.anthropic_client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=settings.MAX_TOKENS,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response = message.content[0].text
        
        return response
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the agent
        
        Returns:
            Dictionary with statistics
        """
        db_stats = self.vectordb_service.get_collection_stats()
        
        return {
            'papers_processed': len(self.papers_metadata),
            'chunks_indexed': db_stats['count'],
            'collection_name': db_stats['name']
        }

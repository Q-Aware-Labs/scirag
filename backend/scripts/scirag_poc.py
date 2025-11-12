"""
SciRAG - Proof of Concept
A simple RAG system that searches arXiv papers and answers questions about them
"""

import os
import arxiv
import fitz  # pymupdf
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict
import anthropic
from datetime import datetime

# Configuration
DOWNLOAD_DIR = Path("./papers")
DOWNLOAD_DIR.mkdir(exist_ok=True)

class SciRAG:
    def __init__(self, anthropic_api_key: str = None):
        """Initialize SciRAG with necessary components"""
        print("🚀 Initializing SciRAG...")
        
        # Setup Anthropic client
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.anthropic_api_key:
            raise ValueError("Please set ANTHROPIC_API_KEY environment variable or pass it as parameter")
        
        self.client = anthropic.Anthropic(api_key=self.anthropic_api_key)
        
        # Setup ChromaDB with sentence transformers
        print("📊 Loading embedding model (this may take a moment on first run)...")
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"  # Fast and efficient model
        )
        
        # Initialize vector database
        self.chroma_client = chromadb.Client()
        try:
            self.chroma_client.delete_collection("scirag_papers")
        except:
            pass
        
        self.collection = self.chroma_client.create_collection(
            name="scirag_papers",
            embedding_function=self.embedding_function
        )
        
        self.papers_metadata = {}
        print("✅ SciRAG initialized successfully!\n")
    
    def search_arxiv(self, query: str, max_results: int = 3) -> List[arxiv.Result]:
        """Search arXiv for relevant papers"""
        print(f"🔍 Searching arXiv for: '{query}'")
        print(f"   Looking for top {max_results} papers...\n")
        
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = list(search.results())
        
        print(f"✅ Found {len(results)} papers:\n")
        for i, paper in enumerate(results, 1):
            print(f"   {i}. {paper.title}")
            print(f"      Authors: {', '.join([a.name for a in paper.authors[:3]])}")
            print(f"      Published: {paper.published.strftime('%Y-%m-%d')}")
            print(f"      URL: {paper.pdf_url}\n")
        
        return results
    
    def download_pdf(self, paper: arxiv.Result) -> Path:
        """Download PDF for a paper"""
        # Create safe filename
        safe_filename = "".join(c for c in paper.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_filename = safe_filename[:100]  # Limit length
        pdf_path = DOWNLOAD_DIR / f"{safe_filename}.pdf"
        
        if pdf_path.exists():
            print(f"   📄 PDF already exists: {pdf_path.name}")
            return pdf_path
        
        print(f"   📥 Downloading: {paper.title[:60]}...")
        
        try:
            # Try the built-in download method
            paper.download_pdf(filename=str(pdf_path))
        except Exception as e:
            # If that fails, construct the PDF URL manually from the entry_id
            print(f"   ⚠️  Standard download failed, trying alternative method...")
            import requests
            
            # Extract arXiv ID from entry_id (format: http://arxiv.org/abs/2301.12345v1)
            arxiv_id = paper.entry_id.split('/abs/')[-1]
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            
            print(f"   📥 Downloading from: {pdf_url}")
            response = requests.get(pdf_url, timeout=30)
            
            if response.status_code == 200:
                with open(pdf_path, 'wb') as f:
                    f.write(response.content)
            else:
                raise Exception(f"Failed to download PDF: HTTP {response.status_code}")
        
        print(f"   ✅ Downloaded to: {pdf_path.name}")
        
        return pdf_path
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF"""
        print(f"   📖 Extracting text from PDF...")
        
        try:
            doc = fitz.open(pdf_path)
            text = ""
            page_count = len(doc)
            
            for page_num in range(page_count):
                try:
                    page = doc[page_num]
                    page_text = page.get_text()
                    text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                except Exception as e:
                    print(f"   ⚠️  Error reading page {page_num + 1}: {e}")
                    continue
            
            doc.close()
            
            if not text.strip():
                print(f"   ⚠️  No text extracted from PDF")
                return ""
            
            print(f"   ✅ Extracted {len(text):,} characters from {page_count} pages")
            return text
        
        except Exception as e:
            print(f"   ❌ Error extracting text: {e}")
            # Try alternative extraction method
            try:
                print(f"   🔄 Trying alternative extraction method...")
                doc = fitz.open(str(pdf_path))
                text = ""
                for page in doc:
                    text += page.get_text("text")
                doc.close()
                
                if text.strip():
                    print(f"   ✅ Alternative method succeeded: {len(text):,} characters")
                    return text
                else:
                    print(f"   ❌ Alternative method also failed")
                    return ""
            except Exception as e2:
                print(f"   ❌ Alternative extraction also failed: {e2}")
                return ""
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if len(chunk.strip()) > 100:  # Only keep substantial chunks
                chunks.append(chunk)
        
        return chunks
    
    def process_paper(self, paper: arxiv.Result) -> bool:
        """Download, extract, and index a paper"""
        print(f"\n📝 Processing: {paper.title[:60]}...")
        
        try:
            # Download PDF
            pdf_path = self.download_pdf(paper)
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            if not text:
                return False
            
            # Chunk text
            print(f"   ✂️  Chunking text...")
            chunks = self.chunk_text(text)
            print(f"   ✅ Created {len(chunks)} chunks")
            
            # Store metadata
            paper_id = paper.entry_id.split('/')[-1]
            self.papers_metadata[paper_id] = {
                'title': paper.title,
                'authors': [a.name for a in paper.authors],
                'published': paper.published.strftime('%Y-%m-%d'),
                'url': paper.pdf_url,
                'summary': paper.summary
            }
            
            # Add to vector database
            print(f"   💾 Adding to vector database...")
            ids = [f"{paper_id}_chunk_{i}" for i in range(len(chunks))]
            metadatas = [{
                'paper_id': paper_id,
                'title': paper.title,
                'chunk_index': i,
                'authors': ', '.join([a.name for a in paper.authors[:3]])
            } for i in range(len(chunks))]
            
            self.collection.add(
                documents=chunks,
                ids=ids,
                metadatas=metadatas
            )
            
            print(f"   ✅ Successfully processed paper!\n")
            return True
            
        except Exception as e:
            print(f"   ❌ Error processing paper: {e}\n")
            return False
    
    def retrieve_relevant_chunks(self, query: str, n_results: int = 5) -> Dict:
        """Retrieve most relevant chunks for a query"""
        print(f"🔎 Retrieving relevant content for: '{query}'")
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        print(f"✅ Found {len(results['documents'][0])} relevant chunks\n")
        
        return results
    
    def generate_response(self, query: str, context_chunks: List[str], metadata: List[Dict]) -> str:
        """Generate response using Claude with RAG context"""
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
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response = message.content[0].text
        
        return response
    
    def query(self, user_question: str, n_chunks: int = 5) -> Dict:
        """Main query method: retrieve and generate"""
        print("="*70)
        print(f"💬 USER QUERY: {user_question}")
        print("="*70 + "\n")
        
        # Retrieve relevant chunks
        results = self.retrieve_relevant_chunks(user_question, n_results=n_chunks)
        
        if not results['documents'][0]:
            return {
                'answer': "I couldn't find any relevant information in the indexed papers.",
                'sources': []
            }
        
        # Generate response
        answer = self.generate_response(
            user_question,
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
            'sources': sources
        }


def main():
    """Main demonstration of SciRAG"""
    
    print("="*70)
    print("                    🧪 SciRAG - Proof of Concept")
    print("          Scientific Research Assistant with RAG")
    print("="*70 + "\n")
    
    # Initialize SciRAG
    try:
        rag = SciRAG()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\n💡 Please set your Anthropic API key:")
        print("   export ANTHROPIC_API_KEY='your-api-key-here'")
        return
    
    # Example usage
    search_topic = "prompt injection"
    
    # Step 1: Search arXiv
    papers = rag.search_arxiv(search_topic, max_results=2)
    
    if not papers:
        print("❌ No papers found. Try a different query.")
        return
    
    # Step 2: Process papers
    print("\n" + "="*70)
    print("                    📚 PROCESSING PAPERS")
    print("="*70)
    
    successful = 0
    for paper in papers:
        if rag.process_paper(paper):
            successful += 1
    
    print(f"\n✅ Successfully processed {successful}/{len(papers)} papers")
    
    if successful == 0:
        print("❌ No papers were successfully processed.")
        return
    
    # Step 3: Ask questions
    print("\n" + "="*70)
    print("                    💡 ASKING QUESTIONS")
    print("="*70 + "\n")
    
    questions = [
        "What are prompt injection attacks and how do they work?",
        "What are the main defense strategies against prompt injection?",
    ]
    
    for question in questions:
        result = rag.query(question)
        
        print("\n" + "-"*70)
        print("📝 ANSWER:")
        print("-"*70)
        print(result['answer'])
        
        print("\n" + "-"*70)
        print("📚 SOURCES:")
        print("-"*70)
        for i, source in enumerate(result['sources'], 1):
            print(f"\n{i}. {source['title']}")
            print(f"   Authors: {', '.join(source['authors'][:3])}")
            print(f"   Published: {source['published']}")
            print(f"   URL: {source['url']}")
        
        print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
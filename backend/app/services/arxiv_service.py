"""
arXiv Service
Handles searching and downloading papers from arXiv
"""

import arxiv
import requests
from pathlib import Path
from typing import List


class ArxivService:
    """Service for interacting with arXiv API"""
    
    def __init__(self, download_dir: Path):
        """Initialize with download directory"""
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True, parents=True)
    
    def search_papers(self, query: str, max_results: int = 3) -> List[arxiv.Result]:
        """
        Search arXiv for relevant papers
        
        Args:
            query: Search query string
            max_results: Maximum number of papers to return
            
        Returns:
            List of arXiv paper results
        """
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
            print(f"      arXiv ID: {paper.entry_id.split('/')[-1]}\n")
        
        return results
    
    def download_pdf(self, paper: arxiv.Result) -> Path:
        """
        Download PDF for a paper
        
        Args:
            paper: arXiv paper result
            
        Returns:
            Path to downloaded PDF file
        """
        # Create safe filename
        safe_filename = "".join(
            c for c in paper.title if c.isalnum() or c in (' ', '-', '_')
        ).rstrip()
        safe_filename = safe_filename[:100]  # Limit length
        pdf_path = self.download_dir / f"{safe_filename}.pdf"
        
        if pdf_path.exists():
            print(f"   📄 PDF already exists: {pdf_path.name}")
            return pdf_path
        
        print(f"   📥 Downloading: {paper.title[:60]}...")
        
        try:
            # Try the built-in download method
            paper.download_pdf(filename=str(pdf_path))
        except Exception as e:
            # If that fails, construct the PDF URL manually
            print(f"   ⚠️  Standard download failed, trying alternative method...")
            
            # Extract arXiv ID from entry_id
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
    
    def get_paper_metadata(self, paper: arxiv.Result) -> dict:
        """
        Extract metadata from a paper
        
        Args:
            paper: arXiv paper result
            
        Returns:
            Dictionary of paper metadata
        """
        return {
            'paper_id': paper.entry_id.split('/')[-1],
            'title': paper.title,
            'authors': [a.name for a in paper.authors],
            'published': paper.published.strftime('%Y-%m-%d'),
            'url': paper.entry_id,
            'pdf_url': f"https://arxiv.org/pdf/{paper.entry_id.split('/')[-1]}.pdf",
            'summary': paper.summary,
            'categories': paper.categories,
        }

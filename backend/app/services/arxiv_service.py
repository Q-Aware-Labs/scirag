"""
arXiv Service
Handles searching and downloading papers from arXiv
"""

import arxiv
import requests
import time
from pathlib import Path
from typing import List


class ArxivService:
    """Service for interacting with arXiv API"""

    def __init__(self, download_dir: Path):
        """Initialize with download directory"""
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True, parents=True)
        self.last_request_time = 0
        self.min_delay = 3.0  # arXiv recommends 3 seconds between requests
    
    def _rate_limit(self):
        """Enforce rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_delay:
            sleep_time = self.min_delay - elapsed
            print(f"   ⏳ Rate limiting: waiting {sleep_time:.1f}s...")
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def search_papers(self, query: str, max_results: int = 3) -> List[arxiv.Result]:
        """
        Search arXiv for relevant papers with rate limiting and retry logic

        Args:
            query: Search query string
            max_results: Maximum number of papers to return

        Returns:
            List of arXiv paper results
        """
        print(f"🔍 Searching arXiv for: '{query}'")
        print(f"   Looking for top {max_results} papers...\n")

        # Rate limiting
        self._rate_limit()

        # Retry logic with exponential backoff
        max_retries = 3
        base_delay = 5.0

        for attempt in range(max_retries):
            try:
                # Create search with page size limit to avoid triggering rate limits
                search = arxiv.Search(
                    query=query,
                    max_results=min(max_results, 50),  # Cap at 50 to avoid rate limits
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

            except Exception as e:
                error_msg = str(e)

                # Check if it's a rate limit error (HTTP 429)
                if "429" in error_msg or "Too Many Requests" in error_msg:
                    if attempt < max_retries - 1:
                        # Exponential backoff
                        wait_time = base_delay * (2 ** attempt)
                        print(f"   ⚠️  Rate limit hit (HTTP 429). Retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise Exception(
                            f"arXiv rate limit exceeded after {max_retries} attempts. "
                            f"Please wait a few minutes before trying again. "
                            f"Tip: Try searching for fewer papers or use more specific search terms."
                        )
                else:
                    # For other errors, raise immediately
                    raise

        # Should not reach here, but just in case
        return []
    
    def download_pdf(self, paper: arxiv.Result) -> Path:
        """
        Download PDF for a paper with rate limiting

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

        # Rate limiting before download
        self._rate_limit()

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

            # Add a small delay before alternative download
            time.sleep(1)

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

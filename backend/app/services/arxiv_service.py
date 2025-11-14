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

    # PDF size limits (50MB max to prevent DoS attacks)
    MAX_PDF_SIZE = 50 * 1024 * 1024  # 50 MB in bytes

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
        Download PDF for a paper with rate limiting and size validation

        Args:
            paper: arXiv paper result

        Returns:
            Path to downloaded PDF file

        Raises:
            ValueError: If PDF exceeds size limit
        """
        import hashlib

        # Create safe filename with hash to prevent collisions
        safe_title = "".join(
            c for c in paper.title if c.isalnum() or c in (' ', '-', '_')
        ).rstrip()
        safe_title = safe_title[:80] if safe_title else "untitled"

        # Add hash of paper ID to ensure uniqueness
        paper_id = paper.entry_id.split('/')[-1]
        id_hash = hashlib.md5(paper_id.encode()).hexdigest()[:8]
        pdf_filename = f"{safe_title}_{id_hash}.pdf"
        pdf_path = self.download_dir / pdf_filename

        # Ensure path stays within download directory (prevent path traversal)
        pdf_path = pdf_path.resolve()
        if not str(pdf_path).startswith(str(self.download_dir.resolve())):
            raise ValueError("Invalid file path detected - possible path traversal attempt")

        if pdf_path.exists():
            # Check existing file size
            file_size = pdf_path.stat().st_size
            if file_size > self.MAX_PDF_SIZE:
                pdf_path.unlink()  # Delete oversized file
                raise ValueError(f"Existing PDF exceeds size limit: {file_size / 1024 / 1024:.1f}MB")
            print(f"   📄 PDF already exists: {pdf_path.name}")
            return pdf_path

        print(f"   📥 Downloading: {paper.title[:60]}...")

        # Rate limiting before download
        self._rate_limit()

        # Extract arXiv ID from entry_id
        arxiv_id = paper.entry_id.split('/abs/')[-1]
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

        try:
            # First, check file size with HEAD request
            head_response = requests.head(pdf_url, timeout=10)
            content_length = head_response.headers.get('content-length')

            if content_length:
                content_length = int(content_length)
                if content_length > self.MAX_PDF_SIZE:
                    raise ValueError(
                        f"PDF too large: {content_length / 1024 / 1024:.1f}MB "
                        f"(max: {self.MAX_PDF_SIZE / 1024 / 1024:.0f}MB)"
                    )
                print(f"   📊 PDF size: {content_length / 1024:.1f}KB")

            # Download with streaming to prevent memory issues
            print(f"   📥 Downloading from: {pdf_url}")
            response = requests.get(pdf_url, stream=True, timeout=30)
            response.raise_for_status()

            downloaded_size = 0
            with open(pdf_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    downloaded_size += len(chunk)
                    if downloaded_size > self.MAX_PDF_SIZE:
                        # Delete partial file
                        f.close()
                        if pdf_path.exists():
                            pdf_path.unlink()
                        raise ValueError(
                            f"PDF exceeded size limit during download: {downloaded_size / 1024 / 1024:.1f}MB"
                        )
                    f.write(chunk)

            print(f"   ✅ Downloaded {downloaded_size / 1024:.1f}KB to: {pdf_path.name}")
            return pdf_path

        except requests.exceptions.RequestException as e:
            # Clean up partial download
            if pdf_path.exists():
                pdf_path.unlink()
            raise Exception(f"Failed to download PDF: {str(e)}")
        except Exception as e:
            # Clean up on any error
            if pdf_path.exists():
                pdf_path.unlink()
            raise
    
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

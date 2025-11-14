"""
PDF Service
Handles PDF text extraction and chunking
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import List


class PDFService:
    """Service for PDF processing"""

    # PDF processing limits (50MB max, 500 pages max)
    MAX_PDF_SIZE = 50 * 1024 * 1024  # 50 MB in bytes
    MAX_PAGES = 500  # Maximum pages to process

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize PDF service

        Args:
            chunk_size: Number of words per chunk
            chunk_overlap: Number of overlapping words between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text(self, pdf_path: Path) -> str:
        """
        Extract text from a PDF file with size and page limits

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text as string

        Raises:
            ValueError: If PDF exceeds size or page limits
        """
        # Validate file exists and is readable
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        # Check file size
        file_size = pdf_path.stat().st_size
        if file_size > self.MAX_PDF_SIZE:
            raise ValueError(
                f"PDF too large: {file_size / 1024 / 1024:.1f}MB "
                f"(max: {self.MAX_PDF_SIZE / 1024 / 1024:.0f}MB)"
            )

        print(f"   📖 Extracting text from PDF ({file_size / 1024:.1f}KB)...")

        try:
            doc = fitz.open(pdf_path)
            text = ""
            total_pages = len(doc)

            # Limit number of pages
            page_count = min(total_pages, self.MAX_PAGES)

            if total_pages > self.MAX_PAGES:
                print(f"   ⚠️  Document has {total_pages} pages. Processing first {self.MAX_PAGES}.")

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
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            chunk_size: Number of words per chunk (uses default if None)
            overlap: Number of overlapping words (uses default if None)
            
        Returns:
            List of text chunks
        """
        chunk_size = chunk_size or self.chunk_size
        overlap = overlap or self.chunk_overlap
        
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if len(chunk.strip()) > 100:  # Only keep substantial chunks
                chunks.append(chunk)
        
        return chunks
    
    def process_pdf(self, pdf_path: Path) -> dict:
        """
        Extract and chunk text from a PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with extracted text and chunks
        """
        text = self.extract_text(pdf_path)
        
        if not text:
            return {
                'text': '',
                'chunks': [],
                'success': False
            }
        
        print(f"   ✂️  Chunking text...")
        chunks = self.chunk_text(text)
        print(f"   ✅ Created {len(chunks)} chunks")
        
        return {
            'text': text,
            'chunks': chunks,
            'success': True,
            'char_count': len(text),
            'chunk_count': len(chunks)
        }

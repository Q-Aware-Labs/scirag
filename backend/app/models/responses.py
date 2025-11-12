"""
Response Models
Pydantic schemas for API responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class PaperMetadata(BaseModel):
    """Paper metadata model"""
    paper_id: str
    title: str
    authors: List[str]
    published: str
    url: str
    pdf_url: str
    summary: str
    categories: List[str]


class SearchResponse(BaseModel):
    """Response model for paper search"""
    success: bool
    papers: List[PaperMetadata]
    count: int
    message: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "papers": [
                    {
                        "paper_id": "2301.12345v1",
                        "title": "Attention Is All You Need",
                        "authors": ["Vaswani, Ashish", "Shazeer, Noam"],
                        "published": "2017-06-12",
                        "url": "http://arxiv.org/abs/2301.12345v1",
                        "pdf_url": "https://arxiv.org/pdf/2301.12345v1.pdf",
                        "summary": "The dominant sequence transduction models...",
                        "categories": ["cs.CL", "cs.LG"]
                    }
                ],
                "count": 1,
                "message": "Found 1 paper(s)"
            }
        }


class ProcessResponse(BaseModel):
    """Response model for paper processing"""
    success: bool
    total: int
    processed: int
    failed: int
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "total": 2,
                "processed": 2,
                "failed": 0,
                "message": "Successfully processed 2 out of 2 papers"
            }
        }


class SourceInfo(BaseModel):
    """Source information for RAG responses"""
    title: str
    authors: List[str]
    published: str
    url: str


class QueryResponse(BaseModel):
    """Response model for RAG queries"""
    success: bool
    answer: str
    sources: List[SourceInfo]
    message: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "answer": "Attention mechanisms allow models to focus on relevant parts...",
                "sources": [
                    {
                        "title": "Attention Is All You Need",
                        "authors": ["Vaswani, Ashish"],
                        "published": "2017-06-12",
                        "url": "http://arxiv.org/abs/2301.12345v1"
                    }
                ],
                "message": None
            }
        }


class PaperListResponse(BaseModel):
    """Response model for listing papers"""
    success: bool
    papers: List[PaperMetadata]
    count: int


class StatsResponse(BaseModel):
    """Response model for system statistics"""
    success: bool
    papers_processed: int
    chunks_indexed: int
    collection_name: str


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
    detail: Optional[str] = None

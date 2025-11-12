"""
Request Models
Pydantic schemas for API request validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class SearchRequest(BaseModel):
    """Request model for searching papers"""
    query: str = Field(..., description="Search query for arXiv", min_length=1)
    max_results: Optional[int] = Field(3, description="Maximum number of papers to return", ge=1, le=10)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "attention mechanism transformers",
                "max_results": 3
            }
        }


class ProcessPapersRequest(BaseModel):
    """Request model for processing papers"""
    paper_ids: List[str] = Field(..., description="List of arXiv paper IDs to process")
    
    class Config:
        json_schema_extra = {
            "example": {
                "paper_ids": ["2301.12345v1", "2302.67890v1"]
            }
        }


class QueryRequest(BaseModel):
    """Request model for querying with RAG"""
    question: str = Field(..., description="Question to answer based on indexed papers", min_length=1)
    n_results: Optional[int] = Field(5, description="Number of chunks to retrieve", ge=1, le=20)
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What are attention mechanisms and how do they work?",
                "n_results": 5
            }
        }

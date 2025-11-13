"""
Request Models
Pydantic schemas for API request validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal


class APIConfig(BaseModel):
    """API configuration for LLM providers"""
    provider: Literal["claude", "openai", "deepseek", "gemini"] = Field(
        "claude",
        description="LLM provider to use"
    )
    api_key: str = Field(..., description="API key for the selected provider")
    model: Optional[str] = Field(None, description="Specific model to use (uses provider default if not specified)")

    class Config:
        json_schema_extra = {
            "example": {
                "provider": "claude",
                "api_key": "sk-ant-api03-...",
                "model": "claude-sonnet-4-20250514"
            }
        }


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
    api_config: Optional[APIConfig] = Field(None, description="Custom API configuration (uses default if not provided)")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What are attention mechanisms and how do they work?",
                "n_results": 5,
                "api_config": {
                    "provider": "claude",
                    "api_key": "sk-ant-api03-...",
                    "model": "claude-sonnet-4-20250514"
                }
            }
        }

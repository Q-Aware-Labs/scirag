"""
Request Models
Pydantic schemas for API request validation
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal


class APIConfig(BaseModel):
    """API configuration for LLM providers"""
    provider: Literal["claude", "openai", "deepseek", "gemini"] = Field(
        "claude",
        description="LLM provider to use"
    )
    api_key: str = Field(..., description="API key for the selected provider", min_length=10, max_length=500)
    model: Optional[str] = Field(None, description="Specific model to use (uses provider default if not specified)", max_length=100)

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
    query: str = Field(..., description="Search query for arXiv", min_length=1, max_length=500)
    max_results: Optional[int] = Field(3, description="Maximum number of papers to return", ge=1, le=10)

    @validator('query')
    def validate_query(cls, v):
        """Validate and sanitize query string"""
        # Remove excessive whitespace
        v = ' '.join(v.split())
        if not v or len(v) < 1:
            raise ValueError('Query cannot be empty after sanitization')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "query": "attention mechanism transformers",
                "max_results": 3
            }
        }


class ProcessPapersRequest(BaseModel):
    """Request model for processing papers"""
    paper_ids: List[str] = Field(..., description="List of arXiv paper IDs to process", min_items=1, max_items=20)
    api_config: Optional[APIConfig] = Field(None, description="API configuration required to process papers (prevents using server's API key)")

    @validator('paper_ids')
    def validate_paper_ids(cls, v):
        """Validate paper IDs"""
        # Limit each ID length
        validated_ids = []
        for paper_id in v:
            if len(paper_id) > 50:  # arXiv IDs are much shorter
                raise ValueError(f'Paper ID too long: {paper_id[:20]}...')
            # Remove whitespace
            paper_id = paper_id.strip()
            if paper_id:
                validated_ids.append(paper_id)

        if not validated_ids:
            raise ValueError('At least one valid paper ID required')

        return validated_ids

    class Config:
        json_schema_extra = {
            "example": {
                "paper_ids": ["2301.12345v1", "2302.67890v1"],
                "api_config": {
                    "provider": "claude",
                    "api_key": "sk-ant-api03-...",
                    "model": "claude-sonnet-4-20250514"
                }
            }
        }


class QueryRequest(BaseModel):
    """Request model for querying with RAG"""
    question: str = Field(..., description="Question to answer based on indexed papers", min_length=1, max_length=2000)
    n_results: Optional[int] = Field(5, description="Number of chunks to retrieve", ge=1, le=20)
    api_config: Optional[APIConfig] = Field(None, description="Custom API configuration (uses default if not provided)")

    @validator('question')
    def validate_question(cls, v):
        """Validate and sanitize question string"""
        # Remove excessive whitespace
        v = ' '.join(v.split())
        if not v or len(v) < 1:
            raise ValueError('Question cannot be empty after sanitization')
        return v

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

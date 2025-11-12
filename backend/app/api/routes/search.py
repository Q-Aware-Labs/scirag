"""
Search Routes
Endpoints for searching arXiv papers
"""

from fastapi import APIRouter, HTTPException
from typing import List

from ...models.requests import SearchRequest
from ...models.responses import SearchResponse, PaperMetadata, ErrorResponse

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
async def search_papers(request: SearchRequest):
    """
    Search arXiv for papers
    
    - **query**: Search query string (e.g., "attention mechanism transformers")
    - **max_results**: Maximum number of papers to return (1-10)
    
    Returns list of paper metadata
    """
    try:
        # Get agent instance using lazy initialization
        from ...main import get_agent
        agent = get_agent()
        
        # Search papers
        papers = agent.search_papers(
            query=request.query,
            max_results=request.max_results
        )
        
        if not papers:
            return SearchResponse(
                success=True,
                papers=[],
                count=0,
                message="No papers found for the given query"
            )
        
        # Convert to response format
        paper_list = []
        for paper in papers:
            metadata = agent.arxiv_service.get_paper_metadata(paper)
            paper_list.append(PaperMetadata(**metadata))
        
        return SearchResponse(
            success=True,
            papers=paper_list,
            count=len(paper_list),
            message=f"Found {len(paper_list)} paper(s)"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching papers: {str(e)}"
        )
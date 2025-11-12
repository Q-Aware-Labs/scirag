"""
Papers Routes
Endpoints for processing and managing papers
"""

from fastapi import APIRouter, HTTPException
from typing import Dict

from ...models.requests import ProcessPapersRequest
from ...models.responses import (
    ProcessResponse,
    PaperListResponse,
    PaperMetadata,
    StatsResponse,
    ErrorResponse
)

router = APIRouter()


@router.post("/papers/process", response_model=ProcessResponse)
async def process_papers(request: ProcessPapersRequest):
    """
    Process papers by their arXiv IDs
    
    - **paper_ids**: List of arXiv paper IDs (e.g., ["2301.12345v1", "2302.67890v1"])
    
    Downloads PDFs, extracts text, creates embeddings, and indexes them.
    This must be done before querying with /api/query
    """
    try:
        # Get agent instance using lazy initialization
        from ...main import get_agent
        agent = get_agent()
        
        if not request.paper_ids:
            raise HTTPException(
                status_code=400,
                detail="No paper IDs provided"
            )
        
        # We need to fetch the papers first
        # For now, we'll search for each ID directly
        papers_to_process = []
        
        import arxiv
        for paper_id in request.paper_ids:
            try:
                # Search for specific paper by ID
                search = arxiv.Search(id_list=[paper_id.split('v')[0]])  # Remove version
                results = list(search.results())
                if results:
                    papers_to_process.append(results[0])
            except Exception as e:
                print(f"Warning: Could not fetch paper {paper_id}: {e}")
        
        if not papers_to_process:
            raise HTTPException(
                status_code=404,
                detail="No papers found for the provided IDs"
            )
        
        # Process the papers
        stats = agent.process_papers(papers_to_process)
        
        return ProcessResponse(
            success=stats['successful'] > 0,
            total=stats['total'],
            processed=stats['successful'],
            failed=stats['failed'],
            message=f"Successfully processed {stats['successful']} out of {stats['total']} papers"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing papers: {str(e)}"
        )


@router.get("/papers", response_model=PaperListResponse)
async def list_papers():
    """
    List all processed papers
    
    Returns metadata for all papers that have been indexed
    """
    try:
        # Get agent instance using lazy initialization
        from ...main import get_agent
        agent = get_agent()
        
        papers = []
        for paper_id, metadata in agent.papers_metadata.items():
            papers.append(PaperMetadata(**metadata))
        
        return PaperListResponse(
            success=True,
            papers=papers,
            count=len(papers)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing papers: {str(e)}"
        )


@router.get("/papers/{paper_id}", response_model=PaperMetadata)
async def get_paper(paper_id: str):
    """
    Get details for a specific paper
    
    - **paper_id**: arXiv paper ID (e.g., "2301.12345v1")
    """
    try:
        # Get agent instance using lazy initialization
        from ...main import get_agent
        agent = get_agent()
        
        if paper_id not in agent.papers_metadata:
            raise HTTPException(
                status_code=404,
                detail=f"Paper {paper_id} not found. It may not have been processed yet."
            )
        
        metadata = agent.papers_metadata[paper_id]
        return PaperMetadata(**metadata)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving paper: {str(e)}"
        )


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """
    Get system statistics
    
    Returns information about papers processed and chunks indexed
    """
    try:
        # Get agent instance using lazy initialization
        from ...main import get_agent
        agent = get_agent()
        
        stats = agent.get_stats()
        
        return StatsResponse(
            success=True,
            papers_processed=stats['papers_processed'],
            chunks_indexed=stats['chunks_indexed'],
            collection_name=stats['collection_name']
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting stats: {str(e)}"
        )
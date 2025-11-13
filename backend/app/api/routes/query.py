"""
Query Routes
Endpoints for RAG-based question answering
"""

from fastapi import APIRouter, HTTPException

from ...models.requests import QueryRequest
from ...models.responses import QueryResponse, SourceInfo, ErrorResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_papers(request: QueryRequest):
    """
    Ask a question based on indexed papers (RAG)

    - **question**: Question to answer based on processed papers
    - **n_results**: Number of relevant chunks to retrieve (1-20)
    - **api_config**: Optional custom API configuration (provider, api_key, model)

    Returns answer with source citations

    Note: Papers must be processed first using /api/papers/process
    """
    try:
        # If custom API config is provided, create a new agent instance
        if request.api_config:
            from ...agents.scirag_agent import SciRAGAgent
            import logging

            logger = logging.getLogger(__name__)
            logger.info(f"Creating agent with custom config: provider={request.api_config.provider}, model={request.api_config.model}")

            agent = SciRAGAgent(
                llm_provider=request.api_config.provider,
                llm_api_key=request.api_config.api_key,
                llm_model=request.api_config.model
            )
            logger.info("Agent created successfully with custom config")
        else:
            # Use default agent instance with lazy initialization
            from ...main import get_agent
            agent = get_agent()

        # Check if any papers are indexed
        stats = agent.get_stats()
        if stats['papers_processed'] == 0:
            return QueryResponse(
                success=False,
                answer="",
                sources=[],
                message="No papers have been processed yet. Please search and process papers first using /api/search and /api/papers/process"
            )

        # Query the agent
        result = agent.query(
            question=request.question,
            n_results=request.n_results
        )
        
        if not result['success']:
            return QueryResponse(
                success=False,
                answer=result['answer'],
                sources=[],
                message="Could not find relevant information in indexed papers"
            )
        
        # Convert sources to response format
        sources = [
            SourceInfo(
                title=source['title'],
                authors=source['authors'],
                published=source['published'],
                url=source['url']
            )
            for source in result['sources']
        ]
        
        return QueryResponse(
            success=True,
            answer=result['answer'],
            sources=sources,
            message=None
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )
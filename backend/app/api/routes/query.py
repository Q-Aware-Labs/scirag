"""
Query Routes
Endpoints for RAG-based question answering
"""

import logging
from fastapi import APIRouter, HTTPException

from ...models.requests import QueryRequest
from ...models.responses import QueryResponse, SourceInfo, GuardrailWarning, ErrorResponse
from ...services.guardrails_service import GuardrailsService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize guardrails service with built-in checks
guardrails_service = GuardrailsService()


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
        # ============================================
        # GUARDRAIL CHECK #1: Input Safety
        # ============================================
        is_safe_input, warning_type, warning_msg = guardrails_service.check_input(request.question)

        if not is_safe_input:
            logger.warning(f"Guardrail blocked input: {warning_type}")
            return QueryResponse(
                success=False,
                answer="",
                sources=[],
                message="Your request was blocked for safety reasons.",
                guardrail_warning=GuardrailWarning(
                    type=warning_type,
                    message=warning_msg,
                    severity="error"
                )
            )

        # If custom API config is provided, create a new agent instance
        if request.api_config:
            from ...agents.scirag_agent import SciRAGAgent

            logger.info(f"Creating agent with custom config: provider={request.api_config.provider}")

            agent = SciRAGAgent(
                llm_provider=request.api_config.provider,
                llm_api_key=request.api_config.api_key,
                llm_model=request.api_config.model
            )
            logger.info("Agent created successfully with custom config")
        else:
            # Use default agent instance with lazy initialization
            from ...main import get_agent
            from ...config import settings

            # Check if server has a default API key configured
            if not settings.ANTHROPIC_API_KEY:
                return QueryResponse(
                    success=False,
                    answer="",
                    sources=[],
                    message="No API key provided. Please configure your API key in the Configuration tab to use the query feature."
                )

            agent = get_agent()

        # Check if any papers are indexed in ChromaDB
        # Note: We check chunks_indexed instead of papers_processed because when using
        # custom API config, a new agent instance is created which doesn't have the
        # in-memory papers_metadata, but ChromaDB still has all the processed papers
        stats = agent.get_stats()
        if stats['chunks_indexed'] == 0:
            return QueryResponse(
                success=False,
                answer="",
                sources=[],
                message="No papers have been processed yet. Please search and process papers first using /api/search and /api/papers/process"
            )

        # Query the agent (get retrieved context for guardrails check)
        result = agent.query(
            question=request.question,
            n_results=request.n_results
        )

        # ============================================
        # GUARDRAIL CHECK #2: Output Grounding
        # ============================================
        # Get the retrieved documents for checking
        vector_results = agent.vectordb_service.query(request.question, n_results=request.n_results)
        retrieved_docs = vector_results.get('documents', [[]])[0] if vector_results else []

        is_safe_output, out_warning_type, out_warning_msg = guardrails_service.check_output(
            response=result['answer'],
            retrieved_context=retrieved_docs,
            user_question=request.question
        )

        # Create guardrail warning if output check failed
        output_warning = None
        if not is_safe_output:
            logger.warning(f"Guardrail flagged output: {out_warning_type}")
            output_warning = GuardrailWarning(
                type=out_warning_type,
                message=out_warning_msg,
                severity="warning"  # Warning, not error - still return the answer
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
            message=None,
            guardrail_warning=output_warning
        )

    except Exception as e:
        logger.error(f"Query processing failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to process query. Please try again."
        )

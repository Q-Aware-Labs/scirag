"""
SciRAG FastAPI Application
Main application entry point with lazy agent initialization
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from .api.routes import search, query, papers
from .config import settings
from .utils.error_handlers import (
    generic_exception_handler,
    validation_exception_handler,
)

# Global agent instance - initialized lazily
agent = None


def get_agent():
    """
    Get or create the SciRAGAgent instance (lazy initialization).
    This prevents memory issues on startup.
    """
    global agent
    if agent is None:
        print("🔄 Initializing SciRAG Agent (lazy load)...")
        from .agents.scirag_agent import SciRAGAgent
        agent = SciRAGAgent()
        print("✅ SciRAG Agent initialized")
    return agent


# Create FastAPI app without lifespan (to avoid startup memory spike)
app = FastAPI(
    title="SciRAG API",
    description="Scientific Research Assistant with RAG - API for searching arXiv papers and answering questions",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # Configured via ALLOWED_ORIGINS env var
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Only needed HTTP methods
    allow_headers=["Content-Type", "Authorization"],
)

# Register error handlers to sanitize error messages
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include routers
app.include_router(search.router, prefix="/api", tags=["Search"])
app.include_router(query.router, prefix="/api", tags=["Query"])
app.include_router(papers.router, prefix="/api", tags=["Papers"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to SciRAG API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "api_endpoints": {
            "search": "/api/search",
            "query": "/api/query",
            "papers": "/api/papers",
            "process": "/api/process"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns basic health without initializing heavy resources.
    """
    return {
        "status": "healthy",
        "version": "0.1.0",
        "message": "SciRAG API is running",
        "config": {
            "max_papers": settings.MAX_PAPERS,
            "claude_model": settings.CLAUDE_MODEL,
            "embedding_model": settings.EMBEDDING_MODEL
        }
    }


@app.get("/api/status")
async def agent_status():
    """
    Get agent initialization status.
    This will initialize the agent if it hasn't been already.
    """
    global agent

    try:
        agent_instance = get_agent()
        stats = agent_instance.get_stats()
        return {
            "status": "initialized",
            "agent_stats": stats
        }
    except Exception as e:
        # Log error internally but don't expose details
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to initialize agent: {str(e)}", exc_info=True)

        return {
            "status": "error",
            "message": "Failed to initialize agent. Please check server logs."
        }
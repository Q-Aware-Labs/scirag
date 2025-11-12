"""
SciRAG FastAPI Application
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .api.routes import search, query, papers
from .config import settings

# Global agent instance
agent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager
    Initializes resources on startup, cleans up on shutdown
    """
    global agent
    
    # Startup: Initialize the agent
    print("🚀 Starting SciRAG API...")
    from .agents.scirag_agent import SciRAGAgent
    agent = SciRAGAgent()
    print("✅ SciRAG Agent initialized")
    
    yield
    
    # Shutdown
    print("👋 Shutting down SciRAG API...")


# Create FastAPI app
app = FastAPI(
    title="SciRAG API",
    description="Scientific Research Assistant with RAG - API for searching arXiv papers and answering questions",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global agent
    
    if agent is None:
        return {
            "status": "unhealthy",
            "message": "Agent not initialized"
        }
    
    try:
        stats = agent.get_stats()
        return {
            "status": "healthy",
            "version": "0.1.0",
            "agent_stats": stats
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": str(e)
        }


# Global agent instance accessible to routes
agent = None

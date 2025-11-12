"""
Agent accessor helper
Provides lazy access to the SciRAG agent across routes
"""

# Import will be done at runtime to avoid circular imports
_agent = None


def get_agent():
    """
    Get the SciRAG agent instance with lazy initialization.
    
    Returns:
        SciRAGAgent: The initialized agent instance
    """
    global _agent
    
    if _agent is None:
        print("🔄 Initializing SciRAG Agent...")
        from app.agents.scirag_agent import SciRAGAgent
        _agent = SciRAGAgent()
        print("✅ SciRAG Agent initialized")
    
    return _agent
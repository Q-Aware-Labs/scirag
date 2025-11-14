"""
Configuration management for SciRAG
Loads settings from .env file
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings"""

    # Security - CORS Configuration
    ALLOWED_ORIGINS: list = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000"  # Default for local development
    ).split(",")

    # API Keys (optional - users can provide their own via the UI)
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # arXiv Settings
    MAX_PAPERS: int = int(os.getenv("MAX_PAPERS", "5"))

    # PDF Processing
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    DOWNLOAD_DIR: Path = Path(os.getenv("DOWNLOAD_DIR", "./papers"))

    # Embedding Settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # Vector DB Settings
    CHROMA_PERSIST_DIR: Path = Path(os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"))

    # LLM Settings
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2000"))

    def __init__(self):
        """Validate settings on initialization"""
        # API key is now optional - users can provide their own via the UI
        # No longer raising an error if ANTHROPIC_API_KEY is not set

        # Create directories if they don't exist
        self.DOWNLOAD_DIR.mkdir(exist_ok=True, parents=True)
        self.CHROMA_PERSIST_DIR.mkdir(exist_ok=True, parents=True)
    
    def __repr__(self):
        """String representation (hide API key)"""
        return (
            f"Settings(\n"
            f"  ANTHROPIC_API_KEY={'*' * 20}\n"
            f"  MAX_PAPERS={self.MAX_PAPERS}\n"
            f"  CHUNK_SIZE={self.CHUNK_SIZE}\n"
            f"  EMBEDDING_MODEL={self.EMBEDDING_MODEL}\n"
            f"  CLAUDE_MODEL={self.CLAUDE_MODEL}\n"
            f")"
        )


# Global settings instance
settings = Settings()

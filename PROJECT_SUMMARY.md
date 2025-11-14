# SciRAG - Scientific Research Assistant

## Overview
A Retrieval-Augmented Generation (RAG) system that enables semantic search and intelligent querying of scientific papers from arXiv.

## Tech Stack

**Backend** (Python)
- FastAPI for REST API
- ChromaDB for vector embeddings storage
- OpenAI API (GPT-4) for natural language processing
- PyMuPDF for PDF text extraction
- arXiv API for paper retrieval

**Frontend** (TypeScript)
- React 18 with Vite
- TailwindCSS for styling
- Axios for API communication

**Deployment**
- Railway (Backend API)
- Vercel (Frontend)

## Architecture

1. **Search & Retrieval**: Query arXiv database, download papers
2. **Processing**: Extract text from PDFs, generate embeddings
3. **Vector Storage**: Store embeddings in ChromaDB for semantic search
4. **RAG Pipeline**: Retrieve relevant context, generate answers using GPT-4
5. **Built-in Guardrails**: Content safety and response validation

## Key Features
- Semantic search across scientific papers
- Context-aware question answering
- PDF processing with size and page limits (50MB, 500 pages)
- Input validation and sanitized error handling
- CORS security with configurable origins
- Rate limiting and retry logic for API calls

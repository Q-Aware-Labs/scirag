# 📂 File Placement Guide
## From POC to Production Structure

## 🎯 Quick Overview

```
SCIRAG/
├── backend/
│   ├── app/
│   │   ├── __init__.py                    # NEW - Create empty file
│   │   ├── main.py                        # NEW - FastAPI app (create later)
│   │   ├── agents/
│   │   │   ├── __init__.py                # NEW - Create empty file
│   │   │   └── scirag_agent.py            # PUT: Modified scirag_poc.py logic
│   │   ├── api/
│   │   │   ├── __init__.py                # NEW - Create empty file
│   │   │   └── routes/
│   │   │       ├── __init__.py            # NEW - Create empty file
│   │   │       ├── search.py              # NEW - Create later
│   │   │       └── query.py               # NEW - Create later
│   │   ├── models/
│   │   │   ├── __init__.py                # NEW - Create empty file
│   │   │   ├── requests.py                # NEW - Create later
│   │   │   └── responses.py               # NEW - Create later
│   │   ├── services/
│   │   │   ├── __init__.py                # NEW - Create empty file
│   │   │   ├── arxiv_service.py           # PUT: Extract from scirag_poc.py
│   │   │   ├── pdf_service.py             # PUT: Extract from scirag_poc.py
│   │   │   ├── embedding_service.py       # PUT: Extract from scirag_poc.py
│   │   │   └── vectordb_service.py        # PUT: Extract from scirag_poc.py
│   │   ├── config.py                      # PUT: .env.example logic
│   │   └── tests/
│   │       ├── __init__.py                # NEW - Create empty file
│   │       ├── test_scirag.py             # PUT: test_scirag.py (modified)
│   │       └── test_services.py           # NEW - Create later
│   ├── scripts/
│   │   ├── scirag_poc.py                  # PUT: scirag_poc.py (keep as standalone demo)
│   │   └── scirag_interactive.py          # PUT: scirag_interactive.py (keep as standalone demo)
│   ├── requirements.txt                    # PUT: requirements.txt
│   ├── .env.example                        # PUT: .env.example
│   └── .gitignore                          # PUT: .gitignore
├── frontend/                               # Will create later
├── docs/
│   ├── README.md                           # PUT: README.md
│   ├── USAGE.md                            # PUT: USAGE.md
│   ├── ROADMAP.md                          # PUT: ROADMAP.md
│   └── PROJECT_STRUCTURE.md                # PUT: PROJECT_STRUCTURE.md
├── papers/                                 # Created automatically when scripts run
├── venv/                                   # Create with: python -m venv venv
└── docker-compose.yml                      # NEW - Create later
```

## 📝 Detailed File Placement

### 1. Root Level Files

```bash
SCIRAG/
├── .gitignore                    # PUT: .gitignore from POC
├── docker-compose.yml            # CREATE LATER (see Phase 5)
└── README.md                     # OPTION: Put main README here or in docs/
```

### 2. Documentation (Create /docs folder)

```bash
SCIRAG/docs/
├── README.md                     # PUT: README.md from POC
├── USAGE.md                      # PUT: USAGE.md from POC
├── ROADMAP.md                    # PUT: ROADMAP.md from POC
└── PROJECT_STRUCTURE.md          # PUT: PROJECT_STRUCTURE.md from POC
```

### 3. Backend Configuration Files

```bash
SCIRAG/backend/
├── requirements.txt              # PUT: requirements.txt from POC
└── .env.example                  # PUT: .env.example from POC
```

### 4. Backend App Structure

#### Core Logic → agents/

```bash
SCIRAG/backend/app/agents/
└── scirag_agent.py               # REFACTOR: scirag_poc.py SciRAG class
```

The `SciRAG` class from `scirag_poc.py` becomes the agent.

#### Service Layer → services/

```bash
SCIRAG/backend/app/services/
├── arxiv_service.py              # EXTRACT: arXiv methods from scirag_poc.py
├── pdf_service.py                # EXTRACT: PDF processing methods
├── embedding_service.py          # EXTRACT: Embedding methods
└── vectordb_service.py           # EXTRACT: ChromaDB methods
```

#### Configuration → config.py

```bash
SCIRAG/backend/app/config.py      # CREATE: Based on .env.example
```

#### Tests → tests/

```bash
SCIRAG/backend/app/tests/
└── test_scirag.py                # PUT: Modified test_scirag.py
```

### 5. Standalone Scripts (For Testing/Demos)

```bash
SCIRAG/backend/scripts/
├── scirag_poc.py                 # PUT: Keep original POC for demos
└── scirag_interactive.py         # PUT: Keep for quick testing
```

These stay as standalone scripts for quick testing without the API.

---

## 🚀 Step-by-Step Migration

### Phase 1: Initial Setup (Do This Now)

```bash
# 1. Create the folder structure
cd SCIRAG

mkdir -p backend/app/agents
mkdir -p backend/app/api/routes
mkdir -p backend/app/models
mkdir -p backend/app/services
mkdir -p backend/app/tests
mkdir -p backend/scripts
mkdir -p docs
mkdir -p frontend

# 2. Create __init__.py files
touch backend/app/__init__.py
touch backend/app/agents/__init__.py
touch backend/app/api/__init__.py
touch backend/app/api/routes/__init__.py
touch backend/app/models/__init__.py
touch backend/app/services/__init__.py
touch backend/app/tests/__init__.py

# 3. Place POC files
cp requirements.txt backend/
cp .env.example backend/
cp .gitignore ./
cp README.md docs/
cp USAGE.md docs/
cp ROADMAP.md docs/
cp PROJECT_STRUCTURE.md docs/

# 4. Keep POC scripts as standalone demos
cp scirag_poc.py backend/scripts/
cp scirag_interactive.py backend/scripts/
cp test_scirag.py backend/app/tests/
```

### Phase 2: Refactor POC into Services (Do This Next)

Now we'll break down `scirag_poc.py` into separate service files.

#### Create: backend/app/services/arxiv_service.py

```python
"""
arXiv search service
Extract the arXiv-related methods from scirag_poc.py
"""
import arxiv
from typing import List

class ArxivService:
    def search_papers(self, query: str, max_results: int = 3) -> List[arxiv.Result]:
        """Search arXiv for papers"""
        # Copy the search_arxiv method from scirag_poc.py
        pass
    
    def download_pdf(self, paper: arxiv.Result, download_dir: str) -> str:
        """Download PDF for a paper"""
        # Copy the download_pdf method from scirag_poc.py
        pass
```

#### Create: backend/app/services/pdf_service.py

```python
"""
PDF processing service
Extract PDF-related methods from scirag_poc.py
"""
import fitz
from typing import List

class PDFService:
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF"""
        # Copy extract_text_from_pdf method from scirag_poc.py
        pass
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Chunk text into smaller pieces"""
        # Copy chunk_text method from scirag_poc.py
        pass
```

#### Create: backend/app/services/embedding_service.py

```python
"""
Embedding service
Handle text embeddings
"""
from chromadb.utils import embedding_functions

class EmbeddingService:
    def __init__(self):
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    
    def create_embeddings(self, texts: List[str]):
        """Create embeddings for texts"""
        # Copy relevant logic
        pass
```

#### Create: backend/app/services/vectordb_service.py

```python
"""
Vector database service
Handle ChromaDB operations
"""
import chromadb

class VectorDBService:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = None
    
    def create_collection(self, name: str, embedding_function):
        """Create or get collection"""
        pass
    
    def add_documents(self, documents: List[str], metadatas: List[dict], ids: List[str]):
        """Add documents to collection"""
        pass
    
    def query(self, query_text: str, n_results: int = 5):
        """Query the collection"""
        pass
```

#### Create: backend/app/agents/scirag_agent.py

```python
"""
Main SciRAG Agent
Orchestrates all services
"""
from ..services.arxiv_service import ArxivService
from ..services.pdf_service import PDFService
from ..services.embedding_service import EmbeddingService
from ..services.vectordb_service import VectorDBService
import anthropic

class SciRAGAgent:
    def __init__(self, anthropic_api_key: str):
        self.arxiv_service = ArxivService()
        self.pdf_service = PDFService()
        self.embedding_service = EmbeddingService()
        self.vectordb_service = VectorDBService()
        self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
    
    def process_query(self, user_query: str):
        """Main query processing pipeline"""
        # 1. Search arXiv
        # 2. Process papers
        # 3. Query vector DB
        # 4. Generate response
        pass
```

#### Create: backend/app/config.py

```python
"""
Configuration management
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    anthropic_api_key: str
    max_papers: int = 5
    chunk_size: int = 1000
    chunk_overlap: int = 200
    embedding_model: str = "all-MiniLM-L6-v2"
    chroma_persist_dir: str = "./chroma_db"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Phase 3: Create FastAPI (Do After Refactoring)

#### Create: backend/app/main.py

```python
"""
FastAPI application
"""
from fastapi import FastAPI
from .api.routes import search, query
from .config import settings

app = FastAPI(title="SciRAG API", version="0.1.0")

# Include routers
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(query.router, prefix="/api", tags=["query"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}
```

---

## 📊 File Mapping Summary

| POC File | → | Production Location | Notes |
|----------|---|---------------------|-------|
| `scirag_poc.py` | → | `backend/scripts/scirag_poc.py` | Keep as demo |
| ↳ `SciRAG` class | → | `backend/app/agents/scirag_agent.py` | Refactor into agent |
| ↳ `search_arxiv` | → | `backend/app/services/arxiv_service.py` | Extract method |
| ↳ `download_pdf` | → | `backend/app/services/arxiv_service.py` | Extract method |
| ↳ `extract_text_from_pdf` | → | `backend/app/services/pdf_service.py` | Extract method |
| ↳ `chunk_text` | → | `backend/app/services/pdf_service.py` | Extract method |
| ↳ Vector DB logic | → | `backend/app/services/vectordb_service.py` | Extract logic |
| ↳ Embedding logic | → | `backend/app/services/embedding_service.py` | Extract logic |
| `scirag_interactive.py` | → | `backend/scripts/scirag_interactive.py` | Keep as demo |
| `test_scirag.py` | → | `backend/app/tests/test_scirag.py` | Modify for new structure |
| `requirements.txt` | → | `backend/requirements.txt` | Copy directly |
| `.env.example` | → | `backend/.env.example` | Copy directly |
| `.gitignore` | → | `.gitignore` (root) | Copy directly |
| `README.md` | → | `docs/README.md` | Copy directly |
| `USAGE.md` | → | `docs/USAGE.md` | Copy directly |
| `ROADMAP.md` | → | `docs/ROADMAP.md` | Copy directly |
| `PROJECT_STRUCTURE.md` | → | `docs/PROJECT_STRUCTURE.md` | Copy directly |

---

## 🎯 Recommended Order

1. **Today**: Create folder structure, place files
2. **Day 2**: Refactor POC into services
3. **Day 3**: Create agent orchestrator
4. **Day 4**: Add config.py
5. **Day 5**: Test refactored code
6. **Week 2**: Build FastAPI endpoints
7. **Week 3**: Add frontend

---

## 💡 Pro Tips

1. **Keep POC scripts working**: They're great for quick tests without the API
2. **Test after each refactor**: Make sure services work independently
3. **Use relative imports**: `from ..services import ArxivService`
4. **Add logging**: Use `structlog` for better debugging
5. **Version your API**: Use `/api/v1/` prefix

---

## 🚀 Quick Start Commands

```bash
# Setup
cd SCIRAG/backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Test POC still works
python scripts/scirag_poc.py

# Test interactive mode
python scripts/scirag_interactive.py

# Later: Run API
cd app
uvicorn main:app --reload
```

---

Need help with any specific refactoring step? Let me know!
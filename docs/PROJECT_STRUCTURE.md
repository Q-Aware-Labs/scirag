# 📁 SciRAG Project Structure

```
scirag-poc/
│
├── 📄 scirag_poc.py              # Main POC script (full demo)
├── 📄 scirag_interactive.py      # Interactive mode (ask your questions)
├── 📄 test_scirag.py             # Quick test script
│
├── 📄 requirements.txt            # Python dependencies
├── 📄 .env.example                # Environment variables template
├── 📄 .gitignore                  # Git ignore rules
│
├── 📖 README.md                   # Main documentation
├── 📖 USAGE.md                    # Usage examples & code snippets
├── 📖 ROADMAP.md                  # Evolution to production system
│
├── 📁 papers/                     # Downloaded PDFs (created on first run)
│   ├── Paper_Title_1.pdf
│   └── Paper_Title_2.pdf
│
└── 📁 venv/                       # Virtual environment (create with python -m venv venv)
```

## File Descriptions

### Core Scripts

| File | Purpose | When to Use |
|------|---------|-------------|
| `scirag_poc.py` | Full automated demo | Learning how it works |
| `scirag_interactive.py` | Ask your own questions | Research your own topics |
| `test_scirag.py` | Quick verification | Testing after setup |

### Documentation

| File | Content | For |
|------|---------|-----|
| `README.md` | Setup guide, overview | Getting started |
| `USAGE.md` | Code examples, tips | Coding with SciRAG |
| `ROADMAP.md` | Production evolution | Building full system |

### Configuration

| File | Purpose |
|------|---------|
| `requirements.txt` | Python packages to install |
| `.env.example` | Template for API keys |
| `.gitignore` | Files to exclude from Git |

## Quick Start Flow

```
1. Clone/Download files
   ↓
2. Create venv: python -m venv venv
   ↓
3. Activate: source venv/bin/activate
   ↓
4. Install: pip install -r requirements.txt
   ↓
5. Set API key: export ANTHROPIC_API_KEY='...'
   ↓
6. Run: python scirag_poc.py
   ↓
7. Experiment: python scirag_interactive.py
```

## Next: Build Your Full System

See `ROADMAP.md` for architecture and features to add:

```
POC (now)  →  Backend API  →  Frontend UI  →  Production
  ↓              ↓              ↓              ↓
Simple      FastAPI        React         Docker
Script      + Auth         + Chat        + Cloud
            + Persist      + UI          + Monitor
```

## Dependencies Overview

| Package | Size | Purpose |
|---------|------|---------|
| `arxiv` | ~50KB | Search papers |
| `PyMuPDF` | ~10MB | Extract PDF text |
| `chromadb` | ~20MB | Vector database |
| `anthropic` | ~2MB | Claude API |
| `sentence-transformers` | ~100MB | Local embeddings |

**Total: ~130MB** (embeddings model downloads on first run)

## Data Flow

```
User Query
    ↓
[Search arXiv]
    ↓
[Download PDFs]
    ↓
[Extract Text] → papers/
    ↓
[Chunk Text]
    ↓
[Create Embeddings] → vector DB (memory)
    ↓
[Query Vector DB] ← User Question
    ↓
[Retrieve Chunks]
    ↓
[LLM Generate] → Answer + Sources
    ↓
User Response
```

## Memory Usage

| Component | RAM |
|-----------|-----|
| Base Python | ~50MB |
| Embedding Model | ~200MB |
| ChromaDB | ~50MB |
| PDF Processing | ~100MB per PDF |

**Minimum: 512MB RAM**
**Recommended: 2GB RAM**

## Network Requirements

- Outbound HTTPS (443) for:
  - arXiv API (export.arxiv.org)
  - Anthropic API (api.anthropic.com)
  - Hugging Face (model download, first run only)

## Platform Compatibility

✅ Linux (Ubuntu, Debian, etc.)
✅ macOS (10.15+)
✅ Windows 10/11 (with Python 3.8+)
✅ Cloud (AWS, GCP, Azure)
✅ Docker

## Development Timeline

| Phase | Time | Files to Modify/Add |
|-------|------|---------------------|
| **POC** (current) | Done | - |
| **Local Persistence** | 1-2 days | Add `database.py`, modify `scirag_poc.py` |
| **Basic API** | 3-5 days | Create `app/main.py`, `app/api/` |
| **Frontend** | 5-7 days | Create `frontend/` directory |
| **Production** | 2-3 weeks | Add auth, tests, deployment configs |

## Cost Breakdown (Monthly)

### Development Phase
- **LLM API**: ~$5-10 (testing)
- **Embedding**: $0 (local)
- **Storage**: $0 (local)
- **Total**: ~$5-10/month

### Production Phase (100 users)
- **LLM API**: ~$50-100
- **Embedding**: ~$5-10 (if using API)
- **Hosting**: ~$20-50
- **Database**: ~$10-20
- **Total**: ~$85-180/month

---

Ready to start? → Run `python scirag_poc.py`

Questions? → Check `README.md` and `USAGE.md`

Building production? → Follow `ROADMAP.md`

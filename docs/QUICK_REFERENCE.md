# 📍 Quick File Placement Reference

## 🎯 Where Does Each POC File Go?

```
┌─────────────────────────────────────────────────────────────┐
│                    POC FILES (what you have now)            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              PRODUCTION STRUCTURE (where they go)           │
└─────────────────────────────────────────────────────────────┘

POC File                    →    Production Location
═══════════════════════════════════════════════════════════════

📄 scirag_poc.py           →    📁 backend/scripts/scirag_poc.py
                                (Keep as standalone demo)

📄 scirag_interactive.py   →    📁 backend/scripts/scirag_interactive.py
                                (Keep for quick testing)

📄 test_scirag.py          →    📁 backend/app/tests/test_scirag.py
                                (Modify for new structure)

📄 requirements.txt        →    📁 backend/requirements.txt
                                (Copy directly)

📄 .env.example            →    📁 backend/.env.example
                                (Copy directly)

📄 .gitignore              →    📁 .gitignore (root level)
                                (Copy directly)

📄 README.md               →    📁 docs/README.md
                                (Or keep at root)

📄 USAGE.md                →    📁 docs/USAGE.md

📄 ROADMAP.md              →    📁 docs/ROADMAP.md

📄 PROJECT_STRUCTURE.md    →    📁 docs/PROJECT_STRUCTURE.md
```

---

## 🏗️ Full Production Structure

```
SCIRAG/                                    ← Root project folder
│
├── .gitignore                            ← PUT: .gitignore
├── README.md                             ← OPTIONAL: main README or link to docs/
│
├── 📁 backend/                           ← All Python backend code
│   ├── requirements.txt                  ← PUT: requirements.txt
│   ├── .env.example                      ← PUT: .env.example
│   ├── .env                              ← CREATE: Your actual API keys (don't commit!)
│   │
│   ├── 📁 scripts/                       ← Standalone demo scripts
│   │   ├── scirag_poc.py                 ← PUT: Original POC (keep working)
│   │   └── scirag_interactive.py         ← PUT: Interactive version (keep working)
│   │
│   └── 📁 app/                           ← Main application package
│       ├── __init__.py                   ← CREATE: Empty file
│       ├── main.py                       ← CREATE LATER: FastAPI app
│       ├── config.py                     ← CREATE: Settings from .env
│       │
│       ├── 📁 agents/                    ← Agent orchestration logic
│       │   ├── __init__.py               ← CREATE: Empty file
│       │   └── scirag_agent.py           ← REFACTOR: From scirag_poc.py
│       │
│       ├── 📁 services/                  ← Business logic services
│       │   ├── __init__.py               ← CREATE: Empty file
│       │   ├── arxiv_service.py          ← EXTRACT: From scirag_poc.py
│       │   ├── pdf_service.py            ← EXTRACT: From scirag_poc.py
│       │   ├── embedding_service.py      ← EXTRACT: From scirag_poc.py
│       │   └── vectordb_service.py       ← EXTRACT: From scirag_poc.py
│       │
│       ├── 📁 api/                       ← REST API endpoints
│       │   ├── __init__.py               ← CREATE: Empty file
│       │   └── 📁 routes/
│       │       ├── __init__.py           ← CREATE: Empty file
│       │       ├── search.py             ← CREATE LATER: Search endpoint
│       │       ├── query.py              ← CREATE LATER: Query endpoint
│       │       └── papers.py             ← CREATE LATER: Papers endpoint
│       │
│       ├── 📁 models/                    ← Data models (Pydantic)
│       │   ├── __init__.py               ← CREATE: Empty file
│       │   ├── requests.py               ← CREATE LATER: Request schemas
│       │   └── responses.py              ← CREATE LATER: Response schemas
│       │
│       └── 📁 tests/                     ← Test files
│           ├── __init__.py               ← CREATE: Empty file
│           ├── test_scirag.py            ← PUT: Modified test_scirag.py
│           └── test_services.py          ← CREATE LATER: Service tests
│
├── 📁 frontend/                          ← React/Next.js app (later)
│   └── (will create later)
│
├── 📁 docs/                              ← Documentation
│   ├── README.md                         ← PUT: README.md
│   ├── USAGE.md                          ← PUT: USAGE.md
│   ├── ROADMAP.md                        ← PUT: ROADMAP.md
│   ├── PROJECT_STRUCTURE.md              ← PUT: PROJECT_STRUCTURE.md
│   └── FILE_PLACEMENT_GUIDE.md           ← PUT: This file
│
├── 📁 papers/                            ← Downloaded PDFs (auto-created)
│   └── (PDFs go here automatically)
│
└── 📁 venv/                              ← Virtual environment (create it)
    └── (python -m venv venv)
```

---

## ⚡ Quick Setup Commands

### Step 1: Create Structure
```bash
# On Linux/Mac:
bash setup_structure.sh

# On Windows:
setup_structure.bat
```

### Step 2: Move Files
```bash
# Copy POC files
cp requirements.txt backend/
cp .env.example backend/
cp .gitignore ./
cp *.md docs/
cp scirag_poc.py backend/scripts/
cp scirag_interactive.py backend/scripts/
cp test_scirag.py backend/app/tests/
```

### Step 3: Setup Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 4: Test POC Still Works
```bash
# Set your API key
export ANTHROPIC_API_KEY='your-key'  # Windows: set ANTHROPIC_API_KEY=your-key

# Run POC
python scripts/scirag_poc.py
```

---

## 🎯 Current Phase: Initial Setup

✅ **Do Now:**
- [ ] Run setup script to create folders
- [ ] Copy POC files to their locations
- [ ] Create virtual environment
- [ ] Test POC scripts still work
- [ ] Commit to git

❌ **Don't Do Yet:**
- [ ] Refactor into services (do after initial setup works)
- [ ] Create FastAPI endpoints (do after refactoring)
- [ ] Build frontend (do after API works)

---

## 📊 File Categories

| Category | Files | Action |
|----------|-------|--------|
| **Keep As-Is** | `scirag_poc.py`, `scirag_interactive.py` | Copy to `backend/scripts/` |
| **Configuration** | `requirements.txt`, `.env.example`, `.gitignore` | Copy to `backend/` or root |
| **Documentation** | All `.md` files | Move to `docs/` |
| **To Refactor** | Logic inside `scirag_poc.py` | Extract to services (later) |
| **To Create** | `main.py`, routes, models | Build after setup (later) |

---

## 🔄 Migration Phases

```
Phase 1: SETUP (← You are here)
  → Create structure
  → Move files
  → Test POC works

Phase 2: REFACTOR
  → Extract services
  → Create agent
  → Update imports

Phase 3: API
  → Create FastAPI
  → Add endpoints
  → Test API

Phase 4: FRONTEND
  → Create React app
  → Build UI
  → Connect to API

Phase 5: DEPLOY
  → Docker
  → Cloud hosting
  → Monitoring
```

---

## 💡 Pro Tips

1. **Test after each move**: Make sure POC scripts still run
2. **Use relative imports**: When you refactor, use `from ..services import`
3. **Keep POC working**: Don't delete original until refactor is done
4. **Git commit often**: Save progress at each phase
5. **One file at a time**: Don't try to refactor everything at once

---

## 🆘 Troubleshooting

**Q: POC scripts don't work after moving**
A: Check your virtual environment is activated and in the right directory

**Q: Import errors after creating services**
A: Make sure all `__init__.py` files exist

**Q: Can't find modules**
A: Run Python from the correct directory or use `PYTHONPATH`

---

## ✅ Checklist

- [ ] Downloaded all POC files
- [ ] Created folder structure (run setup script)
- [ ] Moved files to correct locations
- [ ] Created virtual environment
- [ ] Installed requirements
- [ ] Set ANTHROPIC_API_KEY
- [ ] Tested `python scripts/scirag_poc.py` works
- [ ] Tested `python scripts/scirag_interactive.py` works
- [ ] Ready to start refactoring!

---

**Ready to begin? Run the setup script and start moving files!** 🚀
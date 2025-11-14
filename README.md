# 🎓 SciRAG - Scientific Research Assistant with RAG

<div align="center">

![SciRAG Banner](https://img.shields.io/badge/SciRAG-Research%20Assistant-FFD700?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMkw0IDhWMTRMMTIgMjBMMjAgMTRWOEwxMiAyWiIgc3Ryb2tlPSIjRkZGIiBzdHJva2Utd2lkdGg9IjIiLz48L3N2Zz4=)

**An AI-powered research assistant that searches arXiv papers, processes PDFs, and answers questions using RAG (Retrieval Augmented Generation)**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2+-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Deployment](https://img.shields.io/badge/Deployed-Railway%20%2B%20Vercel-blueviolet?style=flat-square)](https://scirag.railway.app)

[Live Demo](https://scirag.vercel.app) · [API Docs](https://scirag-production.up.railway.app/docs) · [Report Bug](https://github.com/antonyga/scirag/issues) · [Request Feature](https://github.com/antonyga/scirag/issues)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Design Philosophy](#-design-philosophy)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)
- [Contact](#-contact)

---

## 🌟 Overview

**SciRAG** is a full-stack AI application that revolutionizes how researchers interact with scientific literature. By combining arXiv's vast paper database with Claude AI's advanced reasoning capabilities and RAG (Retrieval Augmented Generation) technology, SciRAG enables users to:

- 🔍 **Search** for research papers using natural language
- 📄 **Process** PDFs automatically with text extraction and chunking
- 💬 **Ask questions** and get AI-powered answers with source citations
- 📚 **Build knowledge** from multiple papers simultaneously
- ⚡ **Save time** by getting instant insights from complex research

Perfect for researchers, students, and professionals who need to quickly understand and synthesize scientific literature.

---

## ✨ Features

### 🔎 **Intelligent Paper Search**
- Natural language queries to arXiv database
- Filter by recency, relevance, and number of results
- Rich metadata including authors, dates, and categories
- Direct links to original papers

### 📚 **Automated PDF Processing**
- Download and extract text from PDFs automatically
- Smart text chunking for optimal context retrieval
- Persistent vector database (ChromaDB) with semantic search
- Handles multiple papers simultaneously

### 💡 **RAG-Powered Q&A**
- Ask questions in natural language
- Get comprehensive answers based on processed papers
- Automatic source citations for every claim
- Context-aware follow-up questions
- **Multi-provider AI support** - Choose your preferred LLM:
  - **Claude** (Anthropic) - Default
  - **OpenAI** (GPT-4, GPT-4o)
  - **DeepSeek** - Cost-effective alternative
  - **Gemini** (Google) - Latest Google AI

### 🔑 **Custom API Key Configuration**
- **Use your own API keys** - No shared costs
- **Browser-based storage** - Keys never stored on servers
- **Provider flexibility** - Switch between AI providers
- **Cost control** - Manage your own usage and expenses
- **Privacy-first** - Direct API calls to providers
- **Default fallback** - Option to use server's default key

### 🎨 **Modern Neobrutalist UI**
- Bold, high-contrast design
- Thick borders and offset shadows
- Dotted background pattern
- Fully responsive
- Accessible color palette

### 🚀 **Production Ready**
- RESTful API with auto-generated documentation (Swagger/OpenAPI)
- Type-safe TypeScript frontend
- Environment-based configuration
- Comprehensive error handling
- Deployed on Railway + Vercel

---

## 🎬 Demo

### Live Application
🌐 **Frontend:** [scirag.vercel.app](https://scirag.vercel.app)  
📡 **API:** [scirag.railway.app](https://scirag.railway.app)  
📖 **API Docs:** [scirag.railway.app/docs](https://scirag.railway.app/docs)

### Screenshots

<div align="center">

| Search Interface | Chat Interface |
|:---:|:---:|
| ![Search](docs/screenshots/search.png) | ![Chat](docs/screenshots/chat.png) |
| *Search arXiv for papers with filters* | *Ask questions and get AI-powered answers* |

| Paper Cards | Sidebar |
|:---:|:---:|
| ![Papers](docs/screenshots/papers.png) | ![Sidebar](docs/screenshots/sidebar.png) |
| *Rich paper metadata and summaries* | *Track processed papers* |

</div>

### Example Workflow

```bash
1. Search: "attention mechanisms in transformers"
2. Select 3-5 relevant papers
3. Click "Process Papers" (30-60 seconds)
4. Ask: "What are the key innovations in these papers?"
5. Get AI-generated answer with source citations
6. Ask follow-ups: "How do they compare?", "What are limitations?"
```

---

## 🛠️ Tech Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[ChromaDB](https://www.trychroma.com/)** - Vector database for embeddings
- **LLM Providers (Multi-provider support):**
  - **[Anthropic Claude](https://www.anthropic.com/)** - Default LLM for Q&A
  - **[OpenAI](https://openai.com/)** - GPT-4, GPT-4o models
  - **[DeepSeek](https://www.deepseek.com/)** - Cost-effective alternative
  - **[Google Gemini](https://deepmind.google/technologies/gemini/)** - Google's AI model
- **[PyMuPDF](https://pymupdf.readthedocs.io/)** - PDF text extraction
- **[arXiv API](https://arxiv.org/help/api)** - Scientific paper search
- **[sentence-transformers](https://www.sbert.net/)** - Text embeddings

### Frontend
- **[React 18](https://react.dev/)** - UI library
- **[TypeScript](https://www.typescriptlang.org/)** - Type safety
- **[Vite](https://vitejs.dev/)** - Build tool & dev server
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS
- **[Axios](https://axios-http.com/)** - HTTP client
- **[Lucide React](https://lucide.dev/)** - Icon library

### Deployment & DevOps
- **[Railway](https://railway.app/)** - Backend hosting
- **[Vercel](https://vercel.com/)** - Frontend hosting
- **[GitHub Actions](https://github.com/features/actions)** - CI/CD (optional)
- **[Docker](https://www.docker.com/)** - Containerization

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                       │
│            React + TypeScript + Tailwind                 │
│         (Neobrutalist Design - Deployed on Vercel)       │
│                                                           │
│  Features: Search | Chat | Config (API Key Setup)        │
└─────────────────────────────────────────────────────────┘
                          │
                          ↓ HTTPS/REST (with optional api_config)
┌─────────────────────────────────────────────────────────┐
│                   FastAPI Backend                        │
│           RESTful API with 8 Endpoints                   │
│           Multi-Provider LLM Support                     │
│              (Deployed on Railway)                       │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┬──────────────┐
        ↓                 ↓                 ↓              ↓
   ┌────────┐       ┌──────────┐     ┌──────────────────────┐
   │ arXiv  │       │ ChromaDB │     │   LLM Providers      │
   │ API    │       │ Vectors  │     │  ┌────────────────┐  │
   └────────┘       └──────────┘     │  │ Claude (Anthropic)│
                                      │  │ OpenAI (GPT-4)  │
                                      │  │ DeepSeek        │
                                      │  │ Google Gemini   │
                                      │  └────────────────┘  │
                                      └──────────────────────┘
```

### Data Flow

1. **Search Phase:**
   ```
   User Query → arXiv API → Paper Metadata → Frontend Display
   ```

2. **Processing Phase:**
   ```
   Paper IDs → PDF Download → Text Extraction → 
   Chunking → Embeddings → ChromaDB Storage
   ```

3. **Query Phase:**
   ```
   User Question → Vector Search (ChromaDB) → 
   Relevant Chunks → Claude AI → Answer + Sources
   ```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **API Key** (at least one of the following):
  - **Anthropic Claude** ([Get one](https://console.anthropic.com/)) - Default
  - **OpenAI** ([Get one](https://platform.openai.com/api-keys))
  - **DeepSeek** ([Get one](https://platform.deepseek.com/))
  - **Google Gemini** ([Get one](https://aistudio.google.com/app/apikey))
- **Git** ([Download](https://git-scm.com/))

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/antonyga/scirag.git
cd scirag
```

#### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Frontend Setup

```bash
# Navigate to frontend
cd ../frontend

# Install dependencies
npm install
```

### Configuration

#### 1. Backend Environment Variables

Create `backend/.env`:

```bash
# API Key (Optional - users can provide their own via UI)
# If not set, users MUST configure their own API key in the frontend
ANTHROPIC_API_KEY=your-api-key-here  # Optional: Default fallback key

# Optional (defaults provided)
MAX_PAPERS=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EMBEDDING_MODEL=all-MiniLM-L6-v2
CLAUDE_MODEL=claude-sonnet-4-20250514
MAX_TOKENS=2000
DOWNLOAD_DIR=./papers
CHROMA_PERSIST_DIR=./chroma_db
```

**Getting API Keys:**
- **Anthropic Claude:** [console.anthropic.com](https://console.anthropic.com/)
- **OpenAI:** [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **DeepSeek:** [platform.deepseek.com](https://platform.deepseek.com/)
- **Google Gemini:** [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

> **Note:** The backend API key is now optional. Users can configure their own API keys via the **Config** tab in the UI, which gives them full control over provider selection and costs.

#### 2. Frontend Environment Variables

Create `frontend/.env.local`:

```bash
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## 💻 Usage

### Running Locally

#### Start Backend (Terminal 1)

```bash
cd backend
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
uvicorn app.main:app --reload
```

Backend runs at: **http://localhost:8000**  
API docs at: **http://localhost:8000/docs**

#### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend runs at: **http://localhost:3000**

### Using the Application

1. **Configure API (Optional but Recommended)**
   - Click the **Config** tab in the header
   - Choose your preferred AI provider:
     - **Claude** (Anthropic) - Best for reasoning
     - **OpenAI** (GPT-4) - Most popular
     - **DeepSeek** - Cost-effective option
     - **Gemini** (Google) - Latest Google AI
   - Enter your API key (masked for security)
   - Optionally specify a custom model
   - Click "Save Configuration"
   - Your key is stored locally in your browser only
   - Toggle "Use default API key" to use server's key instead

2. **Search for Papers**
   - Click the **Search** tab
   - Enter a research topic (e.g., "neural networks", "quantum computing")
   - Adjust the number of papers (1-10)
   - Click "Search"

3. **Process Papers**
   - Papers are auto-selected after search
   - Click "Process X Papers"
   - Wait 30-60 seconds for processing

4. **Ask Questions**
   - Automatically switches to **Chat** tab after processing
   - Type your question
   - Get AI-powered answers with sources (using your configured provider)
   - Ask follow-up questions

### Example Queries

**Search queries:**
- "attention mechanisms in transformers"
- "quantum computing error correction"
- "deep learning for medical imaging"

**Questions to ask:**
- "What are the main findings in these papers?"
- "How do these approaches compare?"
- "What are the limitations mentioned?"
- "Explain the methodology step by step"
- "What are practical applications?"

---

## 📡 API Documentation

### Base URL

**Production:** `https://scirag.railway.app`  
**Local:** `http://localhost:8000`

### Endpoints

#### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy"
}
```

#### `POST /api/search`
Search arXiv for papers

**Request:**
```json
{
  "query": "neural networks",
  "max_results": 3
}
```

**Response:**
```json
{
  "success": true,
  "papers": [...],
  "count": 3
}
```

#### `POST /api/papers/process`
Process papers and create embeddings

**Request:**
```json
{
  "paper_ids": ["2301.12345v1", "2302.67890v1"]
}
```

**Response:**
```json
{
  "success": true,
  "total": 2,
  "processed": 2,
  "failed": 0,
  "message": "Successfully processed 2 papers"
}
```

#### `POST /api/query`
Ask questions about processed papers

**Request:**
```json
{
  "question": "What are neural networks?",
  "n_results": 5,
  "api_config": {
    "provider": "claude",
    "api_key": "sk-ant-api03-...",
    "model": "claude-sonnet-4-20250514"
  }
}
```

> **Note:** The `api_config` parameter is optional. If not provided, the default server API key will be used.
>
> **Supported providers:** `claude`, `openai`, `deepseek`, `gemini`

**Response:**
```json
{
  "success": true,
  "answer": "Neural networks are...",
  "sources": [...]
}
```

#### `GET /api/papers`
List all processed papers

**Response:**
```json
{
  "papers": [...],
  "count": 5
}
```

#### `GET /api/stats`
Get system statistics

**Response:**
```json
{
  "papers_indexed": 5,
  "chunks_stored": 247,
  "collection_name": "scirag_papers"
}
```

### Interactive Documentation

Visit **http://localhost:8000/docs** for interactive Swagger UI with:
- Try-it-out functionality
- Request/response schemas
- Authentication details
- Example values

---

## 🌐 Deployment

### Deploy Backend (Railway)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to production"
   git push
   ```

2. **Create Railway Project**
   - Go to [railway.app](https://railway.app)
   - "New Project" → "Deploy from GitHub"
   - Select `scirag` repository

3. **Configure Service**
   - **Root Directory:** `backend`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables** (Optional)
   ```
   ANTHROPIC_API_KEY=your-key-here  # Optional: Users can use their own keys via UI
   ```

   > **Note:** The API key is now optional. Users can configure their own API keys from any supported provider (Claude, OpenAI, DeepSeek, Gemini) directly in the frontend UI.

5. **Generate Domain**
   - Settings → Networking → Generate Domain
   - Save your URL (e.g., `scirag.railway.app`)

### Deploy Frontend (Vercel)

1. **Create Vercel Project**
   - Go to [vercel.com](https://vercel.com)
   - "New Project" → Import from GitHub
   - Select `scirag` repository

2. **Configure Project**
   - **Framework:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `vite build`
   - **Output Directory:** `dist`

3. **Add Environment Variable**
   ```
   VITE_API_BASE_URL=https://your-railway-app.railway.app/api
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait 1-2 minutes
   - Visit your live URL!

**Detailed guides:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 📁 Project Structure

```
scirag/
├── backend/                      # Python FastAPI backend
│   ├── app/
│   │   ├── agents/              # SciRAG orchestrator
│   │   │   └── scirag_agent.py
│   │   ├── api/                 # REST API routes
│   │   │   └── routes/
│   │   │       ├── search.py
│   │   │       ├── query.py
│   │   │       └── papers.py
│   │   ├── models/              # Pydantic schemas
│   │   │   ├── requests.py
│   │   │   └── responses.py
│   │   ├── services/            # Core business logic
│   │   │   ├── arxiv_service.py
│   │   │   ├── pdf_service.py
│   │   │   ├── vectordb_service.py
│   │   │   └── llm_service.py   # Multi-provider LLM abstraction
│   │   ├── config.py            # Configuration management
│   │   └── main.py              # FastAPI application
│   ├── scripts/                 # Utility scripts
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment template
│
├── frontend/                     # React TypeScript frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── SearchSection.tsx
│   │   │   ├── ChatSection.tsx
│   │   │   ├── ConfigSection.tsx  # API key configuration UI
│   │   │   ├── PaperCard.tsx
│   │   │   └── PapersList.tsx
│   │   ├── api/                 # API client
│   │   │   └── client.ts
│   │   ├── App.tsx              # Main app component
│   │   ├── main.tsx             # Entry point
│   │   └── index.css            # Global styles
│   ├── package.json             # Node dependencies
│   ├── vite.config.ts           # Vite configuration
│   ├── tailwind.config.js       # Tailwind configuration
│   └── .env.example             # Environment template
│
├── docs/                         # Documentation
│   ├── DEPLOYMENT_GUIDE.md
│   ├── API_QUICKSTART.md
│   └── FRONTEND_SETUP.md
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🎨 Design Philosophy

### Neobrutalism

SciRAG features a **neobrutalist** design aesthetic:

- **Thick Borders:** 4px solid black borders on all elements
- **Bold Shadows:** Offset shadows (no blur) for depth
- **High Contrast:** Bright colors on white backgrounds
- **Sharp Corners:** No rounded borders (90° angles)
- **Heavy Typography:** Bold fonts (700-900 weights)
- **Dotted Background:** Subtle pattern for texture

### Color Palette

```css
--neo-pink:   #FE90E8  /* Accents, highlights */
--neo-cyan:   #C0F7FE  /* Search section */
--neo-green:  #99E885  /* Chat, success */
--neo-yellow: #F7CB46  /* Headers, CTAs */
--neo-peach:  #FFDCBB  /* Tags, footer */
--neo-black:  #000000  /* Borders, text */
```

### Design Principles

1. **Brutally Honest UI** - No hidden functionality, everything is visible
2. **Maximum Contrast** - Prioritize readability and accessibility
3. **Bold Interactions** - Clear, unmistakable UI feedback
4. **Geometric Simplicity** - Clean lines and shapes
5. **Playful Seriousness** - Professional but approachable

---

## 🔑 Custom API Key Configuration

SciRAG now supports **custom API key configuration**, allowing users to use their own API keys from multiple LLM providers. This feature gives you:

### Benefits

- **💰 Cost Control** - Use your own API keys instead of sharing server costs
- **🔒 Privacy** - Keys stored locally in browser, never on servers
- **🎯 Provider Choice** - Switch between Claude, OpenAI, DeepSeek, or Gemini
- **⚡ Flexibility** - Different models for different use cases
- **📊 Transparency** - Direct access to your API usage and billing

### Supported Providers

| Provider | Default Model | Best For | Pricing |
|----------|---------------|----------|---------|
| **Claude (Anthropic)** | claude-sonnet-4-20250514 | Complex reasoning, research | [Pricing](https://www.anthropic.com/pricing) |
| **OpenAI** | gpt-4o | General purpose, popular | [Pricing](https://openai.com/pricing) |
| **DeepSeek** | deepseek-chat | Cost-effective alternative | [Pricing](https://platform.deepseek.com/pricing) |
| **Gemini (Google)** | gemini-1.5-pro | Multimodal, latest Google AI | [Pricing](https://ai.google.dev/pricing) |

### How It Works

1. **Frontend UI Configuration**
   - Navigate to the **Config** tab
   - Select your preferred provider
   - Enter your API key (masked for security)
   - Optionally specify a custom model
   - Save configuration (stored in browser localStorage)

2. **Backend Processing**
   - When you ask a question, your API config is sent with the request
   - Backend creates a temporary LLM client with your credentials
   - Response generated using your chosen provider
   - Your API key is used only for that request, never stored on server

3. **Fallback Option**
   - Toggle "Use default API key" to use server's configuration
   - Useful for trying the system before committing to a provider
   - Server admin can optionally provide a default key for shared use

### Security & Privacy

- ✅ **Local Storage Only** - API keys stored in browser localStorage
- ✅ **Direct API Calls** - Keys sent directly to provider, not saved on server
- ✅ **HTTPS Required** - All API communications encrypted
- ✅ **User Control** - Clear configuration, easy to update or remove
- ⚠️ **Browser Data** - Clear browser data will remove saved keys

### Example Configuration

```typescript
{
  "provider": "openai",
  "apiKey": "sk-proj-...",
  "model": "gpt-4o"  // Optional: uses default if not specified
}
```

---

## 🗺️ Roadmap

### Phase 1: Core Features ✅
- [x] arXiv paper search
- [x] PDF processing and extraction
- [x] Vector database integration
- [x] RAG-powered Q&A
- [x] REST API
- [x] Neobrutalist frontend

### Phase 2: Deployment ✅
- [x] Railway backend deployment
- [x] Vercel frontend deployment
- [x] Environment configuration
- [x] Production documentation

### Phase 3: Enhanced Features 🚧
- [x] **Custom API key configuration** - Users can use their own keys
- [x] **Multi-provider LLM support** - Claude, OpenAI, DeepSeek, Gemini
- [ ] User authentication (Clerk/Auth0)
- [ ] Conversation history persistence
- [ ] Export to PDF/Markdown
- [ ] Multiple paper collections
- [ ] Advanced search filters
- [ ] Paper annotations

### Phase 4: Expansion 📋
- [ ] Support for more paper sources (PubMed, bioRxiv, PLOS)
- [ ] Team collaboration features
- [ ] Dark mode
- [ ] Mobile app (React Native)
- [ ] Browser extension
- [ ] API access tiers

### Phase 5: Intelligence 🔮
- [ ] Paper recommendations
- [ ] Trend analysis
- [ ] Citation graphs
- [ ] Automatic literature reviews
- [ ] Research assistant chatbot

---

## 🤝 Contributing

Contributions are what make the open-source community amazing! Any contributions you make are **greatly appreciated**.

### How to Contribute

1. **Fork the Project**
   ```bash
   git clone https://github.com/antonyga/scirag.git
   ```

2. **Create your Feature Branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. **Commit your Changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```

4. **Push to the Branch**
   ```bash
   git push origin feature/AmazingFeature
   ```

5. **Open a Pull Request**

### Development Guidelines

- Follow existing code style
- Add tests for new features
- Update documentation
- Keep commits atomic and descriptive
- Ensure all tests pass before submitting

### Areas for Contribution

- 🐛 **Bug fixes** - Check [Issues](https://github.com/antonyga/scirag/issues)
- ✨ **New features** - See [Roadmap](#-roadmap)
- 📖 **Documentation** - Improve guides and examples
- 🎨 **Design** - UI/UX improvements
- 🧪 **Testing** - Increase test coverage
- 🌍 **Translations** - Multi-language support

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

**MIT License Summary:**
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ⚠️ Liability and warranty limitations

---

## 🙏 Acknowledgments

### Technologies
- **[Anthropic](https://www.anthropic.com/)** - Claude AI API for intelligent Q&A
- **[arXiv](https://arxiv.org/)** - Open access to research papers
- **[ChromaDB](https://www.trychroma.com/)** - Efficient vector database
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[React](https://react.dev/)** - Powerful UI library
- **[Railway](https://railway.app/)** - Simple backend hosting
- **[Vercel](https://vercel.com/)** - Seamless frontend deployment

### Special Thanks
- arXiv for maintaining an open repository of scientific knowledge

---

## 📞 Contact & Support

### Author
**Antony Garcia @ Q-Aware Labs**

- 📧 Email: antony.garcia@qawarelabs.com
- 💼 LinkedIn: [Antony Garcia](https://linkedin.com/in/antonyga)

### Project Links
- 🏠 **Repository:** [github.com/antonyga/scirag](https://github.com/antonyga/scirag)
- 🌐 **Live Demo:** [scirag.vercel.app](https://scirag.vercel.app)
- 📖 **Documentation:** [docs](docs/)
- 🐛 **Issues:** [Report a bug](https://github.com/antonyga/scirag/issues)
- 💡 **Discussions:** [GitHub Discussions](https://github.com/antonyga/scirag/discussions)

### Support the Project

If you find SciRAG helpful, please:
- ⭐ **Star** the repository
- 🐛 **Report bugs** and suggest features
- 🔄 **Share** with researchers and students
- 💬 **Discuss** use cases and improvements
- 🤝 **Contribute** code or documentation

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/antonyga/scirag?style=social)
![GitHub forks](https://img.shields.io/github/forks/antonyga/scirag?style=social)
![GitHub issues](https://img.shields.io/github/issues/antonyga/scirag)
![GitHub pull requests](https://img.shields.io/github/issues-pr/antonyga/scirag)
![GitHub last commit](https://img.shields.io/github/last-commit/antonyga/scirag)
![GitHub repo size](https://img.shields.io/github/repo-size/antonyga/scirag)

---

<div align="center">

**Making scientific research accessible, one paper at a time** 🚀

[⬆ Back to Top](#-scirag---scientific-research-assistant-with-rag)

</div>

---

## 🎓 Citation

If you use SciRAG in your research or project, please cite:

```bibtex
@software{scirag2025,
  author = {Garcia, Antony},
  title = {SciRAG: Scientific Research Assistant with RAG},
  year = {2025},
  url = {https://github.com/antonyga/scirag},
  description = {An AI-powered research assistant for searching and understanding scientific literature from Arxiv papers}
}
```

---

**© 2025 Q-Aware Labs. All rights reserved.**

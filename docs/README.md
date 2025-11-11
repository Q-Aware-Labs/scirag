# 🧪 SciRAG - Proof of Concept

A working prototype of an AI-powered scientific research assistant that searches arXiv, processes papers, and answers questions using RAG (Retrieval Augmented Generation).

## 🎯 What This POC Does

1. **Searches arXiv** for papers based on your query
2. **Downloads PDFs** automatically
3. **Extracts and chunks** text from papers
4. **Creates embeddings** using sentence transformers
5. **Stores in vector database** (ChromaDB)
6. **Retrieves relevant context** for questions
7. **Generates answers** using Claude AI

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Anthropic API key (get one at https://console.anthropic.com/)

### Installation

1. **Clone or download the files**
```bash
# Create a project directory
mkdir scirag-poc
cd scirag-poc

# Copy the files: scirag_poc.py and requirements.txt
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

This will install:
- `arxiv` - Official arXiv API wrapper
- `PyMuPDF` - PDF text extraction
- `chromadb` - Vector database
- `anthropic` - Claude API client
- `sentence-transformers` - Local embeddings model

4. **Set your API key**
```bash
# On macOS/Linux:
export ANTHROPIC_API_KEY='your-api-key-here'

# On Windows (Command Prompt):
set ANTHROPIC_API_KEY=your-api-key-here

# On Windows (PowerShell):
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

### Run the POC

```bash
python scirag_poc.py
```

## 📊 What You'll See

The script will:

1. **Initialize** - Load the embedding model (first run takes ~30 seconds)
2. **Search arXiv** - Find papers about "prompt injection attacks"
3. **Process Papers** - Download and index 2 papers
4. **Answer Questions** - Ask and answer 2 demonstration questions

### Expected Output

```
🚀 Initializing SciRAG...
📊 Loading embedding model...
✅ SciRAG initialized successfully!

🔍 Searching arXiv for: 'prompt injection attacks'
✅ Found 2 papers:
   1. Prompt Injection Attacks and Defenses in LLM-Integrated Applications
   2. ...

📝 Processing: Prompt Injection Attacks and Defenses...
   📥 Downloading...
   📖 Extracting text from PDF...
   ✂️  Chunking text...
   💾 Adding to vector database...
   ✅ Successfully processed paper!

💬 USER QUERY: What are prompt injection attacks and how do they work?
🔎 Retrieving relevant content...
🤖 Generating response with Claude...

📝 ANSWER:
[Claude's comprehensive answer based on the papers]

📚 SOURCES:
1. Prompt Injection Attacks and Defenses in LLM-Integrated Applications
   Authors: ...
   URL: ...
```

## 🎮 Customize Your Test

Edit the `main()` function in `scirag_poc.py`:

```python
# Change the search topic
search_topic = "quantum computing"  # or "transformer models", "computer vision", etc.

# Change number of papers
papers = rag.search_arxiv(search_topic, max_results=3)  # default is 2

# Add your own questions
questions = [
    "Your question here?",
    "Another question?",
]
```

## 🔧 Using SciRAG as a Library

You can import and use the `SciRAG` class in your own code:

```python
from scirag_poc import SciRAG

# Initialize
rag = SciRAG(anthropic_api_key="your-key")

# Search and process papers
papers = rag.search_arxiv("machine learning", max_results=3)
for paper in papers:
    rag.process_paper(paper)

# Ask questions
result = rag.query("What are the latest advances in machine learning?")
print(result['answer'])
print(result['sources'])
```

## 💰 Cost Estimate

For this POC (processing 2 papers, asking 2 questions):

- **Embeddings**: FREE (runs locally using sentence-transformers)
- **Vector DB**: FREE (ChromaDB runs locally)
- **Claude API**: ~$0.02-0.05 per run
  - Input tokens: ~10,000 tokens (context from papers)
  - Output tokens: ~500 tokens per question

**Total cost per run: ~$0.02-0.05**

## 📁 File Structure

After running:

```
scirag-poc/
├── scirag_poc.py          # Main script
├── requirements.txt        # Dependencies
├── README.md              # This file
├── papers/                # Downloaded PDFs (created automatically)
│   ├── Prompt_Injection_Attacks.pdf
│   └── ...
└── venv/                  # Virtual environment
```

## 🐛 Troubleshooting

### Error: "Please set ANTHROPIC_API_KEY"
- Make sure you've set the environment variable
- Verify it's set: `echo $ANTHROPIC_API_KEY` (Unix) or `echo %ANTHROPIC_API_KEY%` (Windows)

### Error: "No module named 'fitz'"
- PyMuPDF imports as 'fitz': `pip install PyMuPDF`

### First run is slow
- The embedding model (~80MB) downloads on first run
- Subsequent runs are much faster

### PDF download fails
- Check your internet connection
- Some papers might be restricted
- Try a different search query

### Out of memory
- Reduce `max_results` to process fewer papers
- The embedding model needs ~1GB RAM

## 🚀 Next Steps

This POC demonstrates the core functionality. To build the full SciRAG system:

1. **Add caching** - Don't reprocess same papers
2. **Better chunking** - Use semantic chunking for better retrieval
3. **User sessions** - Track conversation history
4. **API wrapper** - Build FastAPI endpoints
5. **Frontend UI** - Create React/Streamlit interface
6. **Paper selection** - Let agent decide which papers to process
7. **Multi-query** - Handle follow-up questions better
8. **Persistent storage** - Save vector DB to disk

## 📚 Learn More

- [arXiv API Documentation](https://info.arxiv.org/help/api/index.html)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Sentence Transformers](https://www.sbert.net/)

## 🤝 Questions?

This is a proof of concept to help you understand how the system works. Experiment with different queries, adjust parameters, and see how it performs!

---

**Built with:** Python • arXiv • PyMuPDF • ChromaDB • Sentence Transformers • Claude AI

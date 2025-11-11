# 📖 SciRAG Usage Examples

## Available Scripts

### 1. **scirag_poc.py** - Full Demonstration
Shows the complete workflow with automated demo questions.

```bash
python scirag_poc.py
```

**What it does:**
- Searches for papers on "prompt injection attacks"
- Processes 2 papers automatically
- Asks 2 pre-defined questions
- Shows full detailed output

**Best for:** Understanding how the system works

---

### 2. **scirag_interactive.py** - Interactive Mode
Ask your own questions after processing papers.

```bash
python scirag_interactive.py
```

**What it does:**
- Prompts you for a research topic
- Asks how many papers to process
- Lets you ask unlimited questions
- Type 'sources' to see processed papers
- Type 'quit' to exit

**Best for:** Researching your own topics

**Example session:**
```
What topic would you like to research?
📚 Topic: neural networks

How many papers should I fetch? (1-5, default: 2)
📊 Number: 3

[processes papers...]

❓ Your question: What are the main types of neural networks?
[answer...]

❓ Your question: How do convolutional neural networks work?
[answer...]

❓ Your question: quit
```

---

### 3. **test_scirag.py** - Quick Test
Minimal test to verify everything works.

```bash
python test_scirag.py
```

**What it does:**
- Searches for 1 paper
- Processes it
- Asks 1 simple question
- Shows abbreviated output

**Best for:** Quick verification after setup

---

## Code Examples

### Basic Usage

```python
from scirag_poc import SciRAG

# Initialize
rag = SciRAG(anthropic_api_key="your-key")

# Search and process
papers = rag.search_arxiv("quantum computing", max_results=2)
for paper in papers:
    rag.process_paper(paper)

# Ask questions
result = rag.query("What is quantum entanglement?")
print(result['answer'])
```

### Process Specific Papers

```python
from scirag_poc import SciRAG

rag = SciRAG()

# Get papers
papers = rag.search_arxiv("transformers attention mechanism", max_results=3)

# Process only the first paper
if papers:
    rag.process_paper(papers[0])
    
    # Ask multiple questions
    questions = [
        "How does the attention mechanism work?",
        "What are the advantages of transformers?",
        "What are common applications?"
    ]
    
    for q in questions:
        result = rag.query(q)
        print(f"\nQ: {q}")
        print(f"A: {result['answer']}\n")
```

### Custom Configuration

```python
from scirag_poc import SciRAG

class CustomSciRAG(SciRAG):
    def chunk_text(self, text, chunk_size=2000, overlap=400):
        # Larger chunks for more context
        return super().chunk_text(text, chunk_size, overlap)

rag = CustomSciRAG()
# Use as normal...
```

### Batch Processing

```python
from scirag_poc import SciRAG

rag = SciRAG()

# Process multiple topics
topics = [
    "machine learning",
    "natural language processing",
    "computer vision"
]

for topic in topics:
    print(f"\n{'='*50}")
    print(f"Processing: {topic}")
    print('='*50)
    
    papers = rag.search_arxiv(topic, max_results=1)
    for paper in papers:
        rag.process_paper(paper)

# Now query across all papers
result = rag.query("What are common techniques across ML, NLP, and CV?")
print(result['answer'])
```

### Error Handling

```python
from scirag_poc import SciRAG

try:
    rag = SciRAG()
    
    papers = rag.search_arxiv("deep learning", max_results=3)
    
    if not papers:
        print("No papers found")
    else:
        successful = 0
        for paper in papers:
            try:
                if rag.process_paper(paper):
                    successful += 1
            except Exception as e:
                print(f"Error processing {paper.title}: {e}")
        
        print(f"Successfully processed {successful}/{len(papers)} papers")
        
        if successful > 0:
            result = rag.query("Explain deep learning")
            print(result['answer'])
        else:
            print("No papers were successfully processed")
            
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Get Paper Metadata

```python
from scirag_poc import SciRAG

rag = SciRAG()

# Process papers
papers = rag.search_arxiv("reinforcement learning", max_results=2)
for paper in papers:
    rag.process_paper(paper)

# Access metadata
print("\nIndexed Papers:")
for paper_id, metadata in rag.papers_metadata.items():
    print(f"\nTitle: {metadata['title']}")
    print(f"Authors: {', '.join(metadata['authors'])}")
    print(f"Published: {metadata['published']}")
    print(f"URL: {metadata['url']}")
    print(f"Summary: {metadata['summary'][:200]}...")
```

### Retrieve Without Generating

```python
from scirag_poc import SciRAG

rag = SciRAG()

# ... process papers ...

# Just retrieve relevant chunks without generating answer
results = rag.retrieve_relevant_chunks("attention mechanism", n_results=3)

print("Relevant chunks:")
for chunk, metadata in zip(results['documents'][0], results['metadatas'][0]):
    print(f"\nFrom: {metadata['title']}")
    print(f"Chunk: {chunk[:200]}...")
```

## Tips & Best Practices

### 1. Start Small
- Begin with 1-2 papers to test
- Increase once you understand the output quality

### 2. Specific Queries
Better: "What are the advantages of transformer models over RNNs?"
Worse: "Tell me about transformers"

### 3. Follow-up Questions
The system doesn't maintain conversation context between queries.
Include context in each question:
- "What did the papers say about X?"
- "Based on the processed papers, how does Y work?"

### 4. Check Sources
Always review which papers were used:
```python
result = rag.query("your question")
for source in result['sources']:
    print(source['title'])
```

### 5. Cost Management
- Each query costs ~$0.01-0.02
- Processing papers is one-time cost
- Ask multiple questions on the same papers

### 6. Search Tips
- Use specific technical terms
- Add year for recent papers: "transformers 2023"
- Use author names: "attention Vaswani"
- Combine topics: "few-shot learning language models"

## Common Use Cases

### Literature Review
```python
rag = SciRAG()
papers = rag.search_arxiv("meta-learning few-shot", max_results=5)
for paper in papers:
    rag.process_paper(paper)

questions = [
    "What are the main approaches to few-shot learning?",
    "How do meta-learning algorithms work?",
    "What are the limitations of current methods?",
    "What future research directions are suggested?"
]
```

### Comparative Analysis
```python
rag = SciRAG()

# Process papers from different approaches
rag.search_arxiv("BERT language model", max_results=2)
rag.search_arxiv("GPT language model", max_results=2)

result = rag.query("Compare BERT and GPT architectures")
```

### Technical Explanation
```python
rag = SciRAG()
papers = rag.search_arxiv("backpropagation neural networks", max_results=3)

result = rag.query(
    "Explain backpropagation step-by-step with mathematical details"
)
```

## Next Steps

After mastering the POC, you can:
1. Modify chunking strategies
2. Add paper selection logic
3. Implement conversation history
4. Add caching for frequently accessed papers
5. Build a web API around it
6. Create a frontend interface

See the main README.md for architecture ideas!

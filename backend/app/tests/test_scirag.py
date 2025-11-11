"""
Quick Test Script - Minimal example to verify SciRAG works
"""

from scirag_poc import SciRAG

def quick_test():
    """Quick test with minimal output"""
    
    print("🧪 SciRAG Quick Test\n")
    
    # Initialize
    print("1. Initializing...")
    try:
        rag = SciRAG()
        print("   ✅ Ready\n")
    except ValueError as e:
        print(f"   ❌ {e}")
        return
    
    # Search
    print("2. Searching arXiv...")
    papers = rag.search_arxiv("large language models", max_results=1)
    if not papers:
        print("   ❌ No papers found")
        return
    print(f"   ✅ Found: {papers[0].title[:60]}...\n")
    
    # Process
    print("3. Processing paper...")
    success = rag.process_paper(papers[0])
    if not success:
        print("   ❌ Failed to process")
        return
    print("   ✅ Indexed\n")
    
    # Query
    print("4. Testing query...")
    result = rag.query("What are the key characteristics of large language models?")
    print("   ✅ Response generated\n")
    
    print("-" * 70)
    print("ANSWER:")
    print("-" * 70)
    print(result['answer'][:500] + "..." if len(result['answer']) > 500 else result['answer'])
    print("\n✅ Test completed successfully!")


if __name__ == "__main__":
    quick_test()
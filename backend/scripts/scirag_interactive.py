"""
SciRAG - Interactive Mode
Ask your own questions after processing papers
"""

from scirag_poc import SciRAG
import sys


def interactive_mode():
    """Run SciRAG in interactive mode"""
    
    print("="*70)
    print("        🧪 SciRAG - Interactive Research Assistant")
    print("="*70 + "\n")
    
    # Initialize
    try:
        rag = SciRAG()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\n💡 Please set your Anthropic API key:")
        print("   export ANTHROPIC_API_KEY='your-api-key-here'")
        return
    
    # Get search topic from user
    print("What topic would you like to research?")
    search_topic = input("📚 Topic: ").strip()
    
    if not search_topic:
        print("❌ No topic provided. Exiting.")
        return
    
    # Get number of papers
    print("\nHow many papers should I fetch? (1-5, default: 2)")
    num_papers = input("📊 Number: ").strip()
    try:
        num_papers = int(num_papers) if num_papers else 2
        num_papers = max(1, min(5, num_papers))  # Clamp between 1-5
    except:
        num_papers = 2
    
    print(f"\n🔍 Searching for top {num_papers} papers on '{search_topic}'...\n")
    
    # Search arXiv
    papers = rag.search_arxiv(search_topic, max_results=num_papers)
    
    if not papers:
        print("❌ No papers found. Try a different query.")
        return
    
    # Process papers
    print("\n" + "="*70)
    print("                    📚 PROCESSING PAPERS")
    print("="*70)
    
    successful = 0
    for paper in papers:
        if rag.process_paper(paper):
            successful += 1
    
    print(f"\n✅ Successfully processed {successful}/{len(papers)} papers")
    
    if successful == 0:
        print("❌ No papers were successfully processed.")
        return
    
    # Interactive Q&A
    print("\n" + "="*70)
    print("           💬 INTERACTIVE Q&A - Ask me anything!")
    print("="*70)
    print("\nTips:")
    print("  • Ask specific questions about the papers")
    print("  • Type 'quit', 'exit', or 'q' to end")
    print("  • Type 'sources' to see processed papers")
    print()
    
    while True:
        try:
            question = input("❓ Your question: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using SciRAG! Goodbye.")
                break
            
            if question.lower() == 'sources':
                print("\n📚 Processed Papers:\n")
                for i, (paper_id, meta) in enumerate(rag.papers_metadata.items(), 1):
                    print(f"{i}. {meta['title']}")
                    print(f"   Authors: {', '.join(meta['authors'][:3])}")
                    print(f"   Published: {meta['published']}")
                    print(f"   URL: {meta['url']}\n")
                continue
            
            # Query the system
            print()
            result = rag.query(question)
            
            print("\n" + "-"*70)
            print("📝 ANSWER:")
            print("-"*70)
            print(result['answer'])
            
            print("\n" + "-"*70)
            print("📚 SOURCES:")
            print("-"*70)
            for i, source in enumerate(result['sources'], 1):
                print(f"{i}. {source['title']}")
                print(f"   Authors: {', '.join(source['authors'][:2])}")
            
            print("\n" + "="*70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using SciRAG! Goodbye.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    interactive_mode()

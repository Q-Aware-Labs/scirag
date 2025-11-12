"""
Test script for refactored SciRAG services
Run from backend directory: python -m app.tests.test_refactored
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.agents.scirag_agent import SciRAGAgent


def main():
    """Test the refactored SciRAG agent"""
    
    print("="*70)
    print("        🧪 Testing Refactored SciRAG Agent")
    print("="*70 + "\n")
    
    try:
        # Initialize agent
        agent = SciRAGAgent()
        
        # Search papers
        query = "attention mechanism transformers"
        papers = agent.search_papers(query, max_results=2)
        
        if not papers:
            print("❌ No papers found")
            return
        
        # Process papers
        stats = agent.process_papers(papers)
        
        if stats['successful'] == 0:
            print("❌ No papers were successfully processed")
            return
        
        # Ask questions
        questions = [
            "What are attention mechanisms and how do they work?",
            "What are the main advantages of using attention in neural networks?",
        ]
        
        print("\n" + "="*70)
        print("                    💡 ASKING QUESTIONS")
        print("="*70 + "\n")
        
        for question in questions:
            result = agent.query(question)
            
            print("\n" + "-"*70)
            print("📝 ANSWER:")
            print("-"*70)
            print(result['answer'])
            
            print("\n" + "-"*70)
            print("📚 SOURCES:")
            print("-"*70)
            for i, source in enumerate(result['sources'], 1):
                print(f"\n{i}. {source['title']}")
                print(f"   Authors: {', '.join(source['authors'][:3])}")
                print(f"   Published: {source['published']}")
            
            print("\n" + "="*70 + "\n")
        
        # Show stats
        stats = agent.get_stats()
        print("\n📊 Agent Statistics:")
        print(f"   Papers processed: {stats['papers_processed']}")
        print(f"   Chunks indexed: {stats['chunks_indexed']}")
        print(f"   Collection: {stats['collection_name']}")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

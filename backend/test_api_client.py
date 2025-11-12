"""
API Test Client
Demonstrates how to use the SciRAG API
"""

import requests
import json
import time

# API Base URL
BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("\n" + "="*70)
    print("1. Testing Health Endpoint")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()


def test_search(query="attention mechanism transformers", max_results=2):
    """Test search endpoint"""
    print("\n" + "="*70)
    print("2. Testing Search Endpoint")
    print("="*70)
    
    payload = {
        "query": query,
        "max_results": max_results
    }
    
    print(f"Searching for: '{query}'")
    response = requests.post(f"{BASE_URL}/api/search", json=payload)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['count']} papers:")
        
        paper_ids = []
        for i, paper in enumerate(data['papers'], 1):
            print(f"\n  {i}. {paper['title']}")
            print(f"     ID: {paper['paper_id']}")
            print(f"     Authors: {', '.join(paper['authors'][:2])}")
            paper_ids.append(paper['paper_id'])
        
        return paper_ids
    else:
        print(f"Error: {response.text}")
        return []


def test_process(paper_ids):
    """Test process papers endpoint"""
    print("\n" + "="*70)
    print("3. Testing Process Papers Endpoint")
    print("="*70)
    
    if not paper_ids:
        print("No paper IDs to process")
        return False
    
    payload = {
        "paper_ids": paper_ids
    }
    
    print(f"Processing {len(paper_ids)} papers...")
    print("This may take 30-60 seconds...")
    
    response = requests.post(f"{BASE_URL}/api/papers/process", json=payload)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        return data['success']
    else:
        print(f"Error: {response.text}")
        return False


def test_list_papers():
    """Test list papers endpoint"""
    print("\n" + "="*70)
    print("4. Testing List Papers Endpoint")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/api/papers")
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total papers indexed: {data['count']}")
        
        for i, paper in enumerate(data['papers'], 1):
            print(f"\n  {i}. {paper['title']}")
            print(f"     ID: {paper['paper_id']}")
    else:
        print(f"Error: {response.text}")


def test_query(question="What are attention mechanisms and how do they work?"):
    """Test query endpoint"""
    print("\n" + "="*70)
    print("5. Testing Query Endpoint (RAG)")
    print("="*70)
    
    payload = {
        "question": question,
        "n_results": 5
    }
    
    print(f"Question: {question}")
    print("Generating answer...")
    
    response = requests.post(f"{BASE_URL}/api/query", json=payload)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n" + "-"*70)
        print("ANSWER:")
        print("-"*70)
        print(data['answer'])
        
        print("\n" + "-"*70)
        print("SOURCES:")
        print("-"*70)
        for i, source in enumerate(data['sources'], 1):
            print(f"\n{i}. {source['title']}")
            print(f"   Authors: {', '.join(source['authors'][:2])}")
            print(f"   URL: {source['url']}")
    else:
        print(f"Error: {response.text}")


def test_stats():
    """Test stats endpoint"""
    print("\n" + "="*70)
    print("6. Testing Stats Endpoint")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/api/stats")
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
    else:
        print(f"Error: {response.text}")


def main():
    """Run all tests"""
    print("="*70)
    print("           🧪 SciRAG API Test Client")
    print("="*70)
    print("\nMake sure the API is running:")
    print("  cd backend")
    print("  uvicorn app.main:app --reload")
    print("\nTesting API at:", BASE_URL)
    
    try:
        # Test health
        test_health()
        
        # Test search
        paper_ids = test_search("attention mechanism transformers", max_results=2)
        
        if not paper_ids:
            print("\n❌ No papers found, stopping tests")
            return
        
        # Test process
        success = test_process(paper_ids)
        
        if not success:
            print("\n❌ Failed to process papers, stopping tests")
            return
        
        # Wait a moment for processing to complete
        time.sleep(2)
        
        # Test list papers
        test_list_papers()
        
        # Test query
        test_query("What are attention mechanisms and how do they work?")
        test_query("What are the advantages of using attention in neural networks?")
        
        # Test stats
        test_stats()
        
        print("\n" + "="*70)
        print("✅ All tests completed!")
        print("="*70)
        print("\nYou can now:")
        print("  1. Open http://localhost:8000/docs for interactive API docs")
        print("  2. Use the API endpoints in your own application")
        print("  3. Build a frontend that connects to this API")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("Make sure the API is running:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

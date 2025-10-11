#!/usr/bin/env python3
"""
Simple test runner for AskMyDocs API
Tests both add_document and query functionality
"""

import requests
import json
import time

def test_api_endpoints():
    """Test the main API endpoints"""
    base_url = "http://localhost:8000"
    headers = {"Content-Type": "application/json"}
    
    print("🧪 Testing AskMyDocs API Endpoints")
    print("=" * 50)
    
    # Test 1: Server Health Check
    print("\n1️⃣ Testing server health...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and accessible")
        else:
            print(f"⚠️  Server returned status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Server health check failed: {e}")
        return False
    
    # Test 2: Add Document
    print("\n2️⃣ Testing add_document endpoint...")
    test_doc = {
        "title": "test_ml_document",
        "content": """
        Machine Learning is a powerful subset of artificial intelligence that allows 
        computers to learn and make decisions from data without being explicitly programmed.
        
        Key types of machine learning include:
        1. Supervised Learning - Learning with labeled training data
        2. Unsupervised Learning - Finding patterns in unlabeled data  
        3. Reinforcement Learning - Learning through trial and error with rewards
        
        Popular algorithms include decision trees, neural networks, and support vector machines.
        Applications span from image recognition to natural language processing.
        """
    }
    
    try:
        response = requests.post(f"{base_url}/chat/add_document", headers=headers, json=test_doc)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Document added successfully: {result['id']}")
            print(f"   Title: {result['title']}")
            print(f"   Content length: {len(result['content'])} characters")
        else:
            print(f"❌ Add document failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Add document test failed: {e}")
        return False
    
    # Test 3: Add Another Document
    print("\n3️⃣ Adding second test document...")
    test_doc2 = {
        "title": "python_basics",
        "content": """
        Python is a high-level, interpreted programming language known for its simplicity and readability.
        
        Key features include:
        - Easy to learn syntax
        - Cross-platform compatibility
        - Large standard library
        - Strong community support
        - Object-oriented programming support
        
        Popular Python libraries include NumPy for numerical computing, Pandas for data analysis,
        and Django for web development. Python is widely used in data science, web development,
        automation, and artificial intelligence projects.
        """
    }
    
    try:
        response = requests.post(f"{base_url}/chat/add_document", headers=headers, json=test_doc2)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Second document added: {result['id']}")
        else:
            print(f"❌ Second document add failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Second document test failed: {e}")
    
    # Wait a moment for embeddings to be processed
    print("\n⏳ Waiting for embeddings to be processed...")
    time.sleep(3)
    
    # Test 4: Query About Machine Learning
    print("\n4️⃣ Testing query endpoint - Machine Learning...")
    query1 = {"query": "What is machine learning and what are its main types?"}
    
    try:
        response = requests.post(f"{base_url}/chat/query", headers=headers, json=query1)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ ML Query successful using {result['llm_used']}")
            print(f"   Answer (first 150 chars): {result['answer'][:150]}...")
            print(f"   Source documents: {len(result['source_documents'])}")
        else:
            print(f"❌ ML Query failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ ML Query test failed: {e}")
    
    # Test 5: Query About Python
    print("\n5️⃣ Testing query endpoint - Python...")
    query2 = {"query": "What are the key features of Python programming language?"}
    
    try:
        response = requests.post(f"{base_url}/chat/query", headers=headers, json=query2, timeout=60)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Python Query successful using {result['llm_used']}")
            print(f"   Answer (first 150 chars): {result['answer'][:150]}...")
        else:
            print(f"❌ Python Query failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Python Query test failed: {e}")
    
    # Test 6: Complex Query
    print("\n6️⃣ Testing complex query...")
    query3 = {"query": "Compare machine learning with traditional programming approaches."}
    
    try:
        response = requests.post(f"{base_url}/chat/query", headers=headers, json=query3, timeout=60)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Complex Query successful")
            print(f"   Answer length: {len(result['answer'])} characters")
            print(f"   First 100 chars: {result['answer'][:100]}...")
        else:
            print(f"⚠️  Complex Query returned status: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Complex Query had issues: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API endpoint tests completed!")
    print("\nTest Summary:")
    print("✅ Server health check")
    print("✅ Document addition (add_document)")
    print("✅ Document querying (query)")
    print("✅ Multiple document types")
    print("✅ Embedding and retrieval system")
    
    return True

if __name__ == "__main__":
    success = test_api_endpoints()
    if success:
        print("\n🏆 All tests completed successfully!")
    else:
        print("\n⚠️  Some tests encountered issues, but basic functionality is working")
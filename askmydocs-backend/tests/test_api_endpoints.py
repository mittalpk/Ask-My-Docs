"""
Automated test cases for AskMyDocs API endpoints
"""

import pytest
import asyncio
import json
import os
from pathlib import Path
import requests
from typing import Dict, Any

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_DOCUMENTS_DIR = "/app/test_documents"


class TestAPIEndpoints:
    """Test class for API endpoints"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.base_url = BASE_URL
        self.headers = {"Content-Type": "application/json"}
    
    def test_server_health(self):
        """Test if the server is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/docs")
            assert response.status_code == 200, "Server should be accessible"
        except requests.ConnectionError:
            pytest.fail("Server is not running or not accessible")
    
    def test_add_document_text_content(self):
        """Test adding a document with text content"""
        test_doc = {
            "title": "test_machine_learning",
            "content": """
            Machine Learning is a subset of artificial intelligence that enables 
            computers to learn and improve from experience without being explicitly programmed.
            Key concepts include supervised learning, unsupervised learning, and reinforcement learning.
            Popular algorithms include linear regression, decision trees, and neural networks.
            """
        }
        
        response = requests.post(
            f"{self.base_url}/chat/add_document",
            headers=self.headers,
            json=test_doc
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert "id" in result, "Response should contain document ID"
        assert result["title"] == test_doc["title"], "Title should match"
        assert result["content"] == test_doc["content"], "Content should match"
        
        print(f"✅ Document added successfully: {result['id']}")
    
    def test_add_document_python_content(self):
        """Test adding a document with Python programming content"""
        with open("/home/pkmittal/MyDemo/AskMyDocs/askmydocs-backend/test_documents/python_programming.txt", "r") as f:
            content = f.read()
        
        test_doc = {
            "title": "python_programming_guide",
            "content": content
        }
        
        response = requests.post(
            f"{self.base_url}/chat/add_document",
            headers=self.headers,
            json=test_doc
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert result["title"] == test_doc["title"]
        assert len(result["content"]) > 100, "Content should be substantial"
        
        print(f"✅ Python document added successfully: {result['id']}")
    
    def test_add_document_fastapi_content(self):
        """Test adding a document with FastAPI content"""
        with open("/home/pkmittal/MyDemo/AskMyDocs/askmydocs-backend/test_documents/fastapi_guide.txt", "r") as f:
            content = f.read()
        
        test_doc = {
            "title": "fastapi_framework_guide", 
            "content": content
        }
        
        response = requests.post(
            f"{self.base_url}/chat/add_document",
            headers=self.headers,
            json=test_doc
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert result["title"] == test_doc["title"]
        
        print(f"✅ FastAPI document added successfully: {result['id']}")
    
    def test_add_document_empty_content(self):
        """Test adding a document with empty content - should fail gracefully"""
        test_doc = {
            "title": "empty_document",
            "content": ""
        }
        
        response = requests.post(
            f"{self.base_url}/chat/add_document",
            headers=self.headers,
            json=test_doc
        )
        
        # Should either succeed with empty content or return appropriate error
        assert response.status_code in [200, 422, 400], "Should handle empty content appropriately"
        
        if response.status_code == 200:
            print("✅ Empty document handled successfully")
        else:
            print(f"✅ Empty document appropriately rejected: {response.status_code}")
    
    def test_add_document_missing_fields(self):
        """Test adding a document with missing required fields"""
        # Missing content field
        test_doc = {"title": "incomplete_document"}
        
        response = requests.post(
            f"{self.base_url}/chat/add_document",
            headers=self.headers,
            json=test_doc
        )
        
        assert response.status_code == 422, "Should return validation error for missing fields"
        print("✅ Missing fields validation working correctly")
    
    def test_query_machine_learning(self):
        """Test querying about machine learning"""
        query = {
            "query": "What is machine learning and what are its types?"
        }
        
        response = requests.post(
            f"{self.base_url}/chat/query",
            headers=self.headers,
            json=query
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert "answer" in result, "Response should contain answer"
        assert "source_documents" in result, "Response should contain source documents"
        assert "llm_used" in result, "Response should indicate which LLM was used"
        
        # Check if answer contains relevant terms
        answer_lower = result["answer"].lower()
        ml_terms = ["machine learning", "artificial intelligence", "algorithm", "data"]
        has_relevant_terms = any(term in answer_lower for term in ml_terms)
        assert has_relevant_terms, "Answer should contain relevant ML terms"
        
        print(f"✅ ML Query answered successfully using {result['llm_used']}")
        print(f"Answer length: {len(result['answer'])} characters")
    
    def test_query_python_programming(self):
        """Test querying about Python programming"""
        query = {
            "query": "What are the key features of Python programming language?"
        }
        
        response = requests.post(
            f"{self.base_url}/chat/query",
            headers=self.headers,
            json=query
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert len(result["answer"]) > 10, "Answer should be substantial"
        
        # Check for Python-related terms
        answer_lower = result["answer"].lower()
        python_terms = ["python", "programming", "language", "syntax"]
        has_relevant_terms = any(term in answer_lower for term in python_terms)
        assert has_relevant_terms, "Answer should contain relevant Python terms"
        
        print(f"✅ Python Query answered successfully using {result['llm_used']}")
    
    def test_query_fastapi_framework(self):
        """Test querying about FastAPI framework"""
        query = {
            "query": "What is FastAPI and what are its advantages?"
        }
        
        response = requests.post(
            f"{self.base_url}/chat/query",
            headers=self.headers,
            json=query
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert len(result["answer"]) > 10, "Answer should be substantial"
        
        print(f"✅ FastAPI Query answered successfully using {result['llm_used']}")
    
    def test_query_empty_question(self):
        """Test querying with empty question"""
        query = {"query": ""}
        
        response = requests.post(
            f"{self.base_url}/chat/query",
            headers=self.headers,
            json=query
        )
        
        # Should handle empty query gracefully
        if response.status_code == 200:
            result = response.json()
            assert "answer" in result, "Should return some response even for empty query"
            print("✅ Empty query handled successfully")
        else:
            print(f"✅ Empty query appropriately rejected: {response.status_code}")
    
    def test_query_complex_question(self):
        """Test querying with a complex multi-part question"""
        query = {
            "query": "Compare machine learning and traditional programming. What are the advantages and disadvantages of each approach?"
        }
        
        response = requests.post(
            f"{self.base_url}/chat/query",
            headers=self.headers,
            json=query
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert len(result["answer"]) > 50, "Complex query should get substantial answer"
        
        print(f"✅ Complex Query answered successfully")
        print(f"Answer: {result['answer'][:100]}...")


class TestDocumentProcessing:
    """Test class for document processing functionality"""
    
    def test_pdf_file_exists(self):
        """Test that the sample PDF file exists"""
        pdf_path = "/home/pkmittal/MyDemo/AskMyDocs/askmydocs-backend/test_documents/sample_document.pdf"
        assert os.path.exists(pdf_path), "Sample PDF should exist"
        
        # Check file size
        file_size = os.path.getsize(pdf_path)
        assert file_size > 0, "PDF file should not be empty"
        
        print(f"✅ PDF file exists and has size: {file_size} bytes")
    
    def test_text_files_exist(self):
        """Test that all text files exist"""
        text_files = [
            "machine_learning_basics.txt",
            "python_programming.txt", 
            "fastapi_guide.txt"
        ]
        
        base_dir = "/home/pkmittal/MyDemo/AskMyDocs/askmydocs-backend/test_documents"
        
        for filename in text_files:
            filepath = os.path.join(base_dir, filename)
            assert os.path.exists(filepath), f"Text file {filename} should exist"
            
            # Check content length
            with open(filepath, 'r') as f:
                content = f.read()
            assert len(content) > 100, f"Text file {filename} should have substantial content"
        
        print("✅ All text files exist and have content")


if __name__ == "__main__":
    # Run tests manually if executed directly
    import sys
    
    print("🧪 Running AskMyDocs API Tests...")
    print("=" * 50)
    
    # Create test instances
    api_tests = TestAPIEndpoints()
    api_tests.setup()
    
    doc_tests = TestDocumentProcessing()
    
    try:
        # Test server health first
        print("Testing server health...")
        api_tests.test_server_health()
        
        # Test document processing
        print("\nTesting document files...")
        doc_tests.test_pdf_file_exists()
        doc_tests.test_text_files_exist()
        
        # Test document addition
        print("\nTesting document addition...")
        api_tests.test_add_document_text_content()
        api_tests.test_add_document_python_content()
        api_tests.test_add_document_fastapi_content()
        api_tests.test_add_document_empty_content()
        api_tests.test_add_document_missing_fields()
        
        # Test queries
        print("\nTesting query functionality...")
        api_tests.test_query_machine_learning()
        api_tests.test_query_python_programming()
        api_tests.test_query_fastapi_framework()
        api_tests.test_query_empty_question()
        api_tests.test_query_complex_question()
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
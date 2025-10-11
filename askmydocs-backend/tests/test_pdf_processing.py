"""
Test cases specifically for PDF document processing
"""

import pytest
import requests
import os
from PyPDF2 import PdfReader


class TestPDFProcessing:
    """Test PDF document processing capabilities"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.base_url = "http://localhost:8000"
        self.headers = {"Content-Type": "application/json"}
        self.pdf_path = "/app/test_documents/sample_document.pdf"
    
    def test_pdf_exists_and_readable(self):
        """Test that PDF file exists and is readable"""
        assert os.path.exists(self.pdf_path), "Sample PDF should exist"
        
        # Try to read the PDF
        try:
            reader = PdfReader(self.pdf_path)
            assert len(reader.pages) > 0, "PDF should have at least one page"
            
            # Extract text from first page
            first_page = reader.pages[0]
            text = first_page.extract_text()
            assert len(text) > 0, "PDF should contain extractable text"
            
            print(f"✅ PDF is readable with {len(reader.pages)} pages")
            print(f"First 100 chars: {text[:100]}...")
            
        except Exception as e:
            pytest.fail(f"Failed to read PDF: {e}")
    
    def test_add_pdf_content_as_document(self):
        """Test adding PDF content as a document after manual extraction"""
        # Extract text from PDF
        reader = PdfReader(self.pdf_path)
        full_text = ""
        
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        
        # Create document with extracted content
        test_doc = {
            "title": "sample_pdf_document",
            "content": full_text
        }
        
        response = requests.post(
            f"{self.base_url}/chat/add_document",
            headers=self.headers,
            json=test_doc
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        result = response.json()
        assert result["title"] == test_doc["title"]
        assert len(result["content"]) > 100, "PDF content should be substantial"
        
        print(f"✅ PDF content added as document: {result['id']}")
        print(f"Content length: {len(result['content'])} characters")
    
    def test_query_pdf_content(self):
        """Test querying information from the PDF content"""
        # First add the PDF content (similar to previous test)
        reader = PdfReader(self.pdf_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        
        # Add document
        test_doc = {
            "title": "pdf_content_for_query",
            "content": full_text
        }
        
        add_response = requests.post(
            f"{self.base_url}/chat/add_document",
            headers=self.headers,
            json=test_doc
        )
        
        assert add_response.status_code == 200, "Should add PDF content successfully"
        
        # Now query the content
        query = {
            "query": "What topics are covered in this document?"
        }
        
        query_response = requests.post(
            f"{self.base_url}/chat/query",
            headers=self.headers,
            json=query
        )
        
        assert query_response.status_code == 200, "Query should be successful"
        
        result = query_response.json()
        assert "answer" in result, "Should return an answer"
        assert len(result["answer"]) > 20, "Answer should be substantial"
        
        print(f"✅ PDF content query successful")
        print(f"Query answer: {result['answer'][:150]}...")


if __name__ == "__main__":
    # Manual test execution
    print("🧪 Running PDF Processing Tests...")
    print("=" * 50)
    
    pdf_tests = TestPDFProcessing()
    pdf_tests.setup_method()
    
    try:
        pdf_tests.test_pdf_exists_and_readable()
        pdf_tests.test_add_pdf_content_as_document()
        pdf_tests.test_query_pdf_content()
        
        print("\n🎉 All PDF tests passed!")
        
    except Exception as e:
        print(f"\n❌ PDF test failed: {e}")
        raise
#!/usr/bin/env python3
"""
Demo script showing how to test with any PDF document
Simply drop PDF files in test_pdf_documents folder and run this script
"""

import os
import requests

def demo_pdf_testing():
    """Demonstrate the flexible PDF testing capability"""
    
    print("🎯 AskMyDocs PDF Testing Demo")
    print("=" * 50)
    
    # Check current PDF files
    pdf_folder = "/app/test_pdf_documents"
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    
    print(f"📁 Found {len(pdf_files)} PDF files ready for testing:")
    for i, pdf_file in enumerate(pdf_files, 1):
        file_path = os.path.join(pdf_folder, pdf_file)
        file_size = os.path.getsize(file_path)
        print(f"   {i}. {pdf_file} ({file_size:,} bytes)")
    
    print(f"\n🚀 To test with your own PDF files:")
    print("1. Copy your PDF to: test_pdf_documents/your_file.pdf")
    print("2. Run: docker exec askmydocs-backend python test_pdf_processing_enhanced.py")
    print("3. Query your content via API!")
    
    print(f"\n💡 Example workflow:")
    print("   # Add your PDF")
    print("   cp ~/Documents/my_report.pdf test_pdf_documents/")
    print("   ")
    print("   # Process all PDFs automatically")
    print("   docker exec askmydocs-backend python test_pdf_processing_enhanced.py")
    print("   ")
    print("   # Query the content")
    print('   curl -X POST "http://localhost:8000/chat/query" \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"query": "What are the main findings in my report?"}\'')
    
    # Test with current files
    print(f"\n🧪 Running quick test with current PDFs...")
    
    try:
        # Quick API test
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
            
            # Test a query
            query_response = requests.post(
                "http://localhost:8000/chat/query",
                headers={"Content-Type": "application/json"},
                json={"query": "What topics are covered in the available documents?"},
                timeout=30
            )
            
            if query_response.status_code == 200:
                result = query_response.json()
                print("✅ Query system working")
                print(f"   Sample answer: {result['answer'][:100]}...")
            else:
                print(f"⚠️  Query returned: {query_response.status_code}")
        else:
            print("❌ API server not responding properly")
            
    except Exception as e:
        print(f"⚠️  Could not connect to API: {e}")
    
    print(f"\n🎉 PDF testing system is ready!")
    print("   Drop any PDF files in test_pdf_documents/ folder")
    print("   Run the enhanced processor to test automatically")
    print("   No code changes needed - works with any PDF content!")

if __name__ == "__main__":
    demo_pdf_testing()
#!/usr/bin/env python3
"""
Test runner script for AskMyDocs application
Runs comprehensive automated tests for both API endpoints
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

def check_server_running():
    """Check if the API server is running"""
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

def run_manual_tests():
    """Run tests manually without pytest"""
    print("🧪 Running Manual Tests...")
    print("=" * 60)
    
    try:
        # Import and run the test file
        sys.path.append('/home/pkmittal/MyDemo/AskMyDocs/askmydocs-backend')
        from tests.test_api_endpoints import TestAPIEndpoints, TestDocumentProcessing
        
        # Create test instances
        api_tests = TestAPIEndpoints()
        api_tests.setup()
        doc_tests = TestDocumentProcessing()
        
        test_results = []
        
        # Define test methods to run
        test_methods = [
            ("Server Health Check", api_tests.test_server_health),
            ("PDF File Exists", doc_tests.test_pdf_file_exists),
            ("Text Files Exist", doc_tests.test_text_files_exist),
            ("Add ML Document", api_tests.test_add_document_text_content),
            ("Add Python Document", api_tests.test_add_document_python_content),
            ("Add FastAPI Document", api_tests.test_add_document_fastapi_content),
            ("Query ML Topic", api_tests.test_query_machine_learning),
            ("Query Python Topic", api_tests.test_query_python_programming),
            ("Query FastAPI Topic", api_tests.test_query_fastapi_framework),
        ]
        
        passed_tests = 0
        total_tests = len(test_methods)
        
        for test_name, test_method in test_methods:
            try:
                print(f"\n🔄 Running: {test_name}")
                test_method()
                print(f"✅ PASSED: {test_name}")
                passed_tests += 1
            except Exception as e:
                print(f"❌ FAILED: {test_name} - {str(e)}")
                test_results.append(f"FAILED: {test_name} - {str(e)}")
        
        print("\n" + "=" * 60)
        print(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
        
        if test_results:
            print("\n❌ Failed Tests:")
            for result in test_results:
                print(f"  - {result}")
        
        if passed_tests == total_tests:
            print("🎉 All tests passed successfully!")
            return True
        else:
            print(f"⚠️  {total_tests - passed_tests} tests failed")
            return False
            
    except Exception as e:
        print(f"❌ Error running manual tests: {e}")
        return False

def run_pytest():
    """Run tests using pytest"""
    print("🧪 Running Tests with Pytest...")
    print("=" * 60)
    
    try:
        # Install pytest dependencies in Docker container
        print("Installing test dependencies in Docker container...")
        subprocess.run([
            "docker", "exec", "askmydocs-backend", 
            "pip", "install", "pytest", "pytest-asyncio", "requests"
        ], check=True)
        
        # Run pytest inside Docker container
        result = subprocess.run([
            "docker", "exec", "askmydocs-backend",
            "python", "-m", "pytest", "/app/tests/", "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        return result.returncode == 0
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Pytest execution failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running pytest: {e}")
        return False

def main():
    """Main test runner function"""
    print("🚀 AskMyDocs Automated Test Suite")
    print("=" * 60)
    
    # Check if server is running
    print("Checking if API server is running...")
    if not check_server_running():
        print("❌ API server is not running on http://localhost:8000")
        print("Please start the server with: docker-compose up")
        return False
    
    print("✅ API server is running")
    
    # Wait a moment for server to be fully ready
    time.sleep(2)
    
    # Try pytest first, fall back to manual tests
    print("\nAttempting to run tests with pytest...")
    
    # For now, let's run manual tests since they're more reliable
    success = run_manual_tests()
    
    if success:
        print("\n🎉 Test suite completed successfully!")
        return True
    else:
        print("\n❌ Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
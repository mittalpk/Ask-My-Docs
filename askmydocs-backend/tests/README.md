# AskMyDocs Test Suite

This directory contains automated test cases for the AskMyDocs application, testing both document addition and query functionality.

## 📁 Directory Structure

The tests are organized in the following structure:

```
tests/
├── __init__.py                 # Package initialization
├── test_api_endpoints.py       # Main API endpoint tests
├── test_pdf_processing.py      # PDF processing tests
├── conftest.py                 # Pytest configuration and fixtures
└── README.md                   # This documentation

test_documents/                 # Sample text documents for testing
├── machine_learning_basics.txt
├── python_programming.txt
└── fastapi_guide.txt

test_pdf_documents/            # PDF documents for testing (NEW!)
├── sample_document.pdf
├── technology_overview.pdf
├── business_strategy.pdf
├── research_methodology.pdf
└── README.md                  # PDF testing documentation

test_pdf_processing_enhanced.py # Enhanced PDF processor (NEW!)
create_multiple_pdfs.py        # PDF generation utility (NEW!)
```

## Test Categories

### 1. API Endpoint Tests (`test_api_endpoints.py`)

#### Document Addition Tests:
- ✅ Add document with machine learning content
- ✅ Add document with Python programming content  
- ✅ Add document with FastAPI framework content
- ✅ Handle empty content gracefully
- ✅ Validate missing required fields

#### Query Tests:
- ✅ Query about machine learning concepts
- ✅ Query about Python programming features
- ✅ Query about FastAPI advantages
- ✅ Handle empty queries
- ✅ Process complex multi-part questions

#### Health & Validation Tests:
- ✅ Server accessibility check
- ✅ Response format validation
- ✅ LLM provider verification

### 2. PDF Processing Tests (`test_pdf_processing.py`)

- ✅ PDF file existence and readability
- ✅ Text extraction from PDF documents
- ✅ Adding PDF content as searchable documents
- ✅ Querying information from PDF content

### 3. Document Processing Tests

- ✅ Text file existence validation
- ✅ Content length verification
- ✅ File format handling

## Running the Tests

### Method 1: Using the Test Runner Script (Recommended)

```bash
# Make sure your API server is running
docker-compose up -d

# Run all tests
python run_tests.py
```

### Method 2: Using Pytest (Inside Docker Container)

```bash
# Install pytest dependencies
docker exec askmydocs-backend pip install pytest pytest-asyncio

# Run tests
docker exec askmydocs-backend python -m pytest /app/tests/ -v
```

### Method 3: Manual Test Execution

```bash
# Run individual test files
python tests/test_api_endpoints.py
python tests/test_pdf_processing.py
```

## Test Configuration

- **pytest.ini**: Contains pytest configuration settings
- **Base URL**: `http://localhost:8000` (configurable)
- **Timeout**: 300 seconds for long-running operations
- **Dependencies**: requests, pytest, pytest-asyncio, PyPDF2

## Expected Test Results

When all tests pass, you should see output similar to:

```
🧪 Running Manual Tests...
============================================================
✅ PASSED: Server Health Check
✅ PASSED: PDF File Exists  
✅ PASSED: Text Files Exist
✅ PASSED: Add ML Document
✅ PASSED: Add Python Document
✅ PASSED: Add FastAPI Document
✅ PASSED: Query ML Topic
✅ PASSED: Query Python Topic
✅ PASSED: Query FastAPI Topic

============================================================
📊 Test Results: 9/9 tests passed
🎉 All tests passed successfully!
```

## Test Data

The test suite uses the following sample documents:

1. **machine_learning_basics.txt** - Covers ML concepts, types, and applications
2. **python_programming.txt** - Python language features and libraries
3. **fastapi_guide.txt** - FastAPI framework documentation
4. **sample_document.pdf** - Generated PDF with testing content

## Troubleshooting

### Common Issues:

1. **Server not running**: Ensure `docker-compose up -d` is executed
2. **Connection refused**: Check if port 8000 is available and not blocked
3. **Missing dependencies**: Install required packages in the container
4. **Timeout errors**: Ollama model loading can be slow on first run

### Debug Steps:

1. Check server logs: `docker-compose logs askmydocs-backend`
2. Verify Ollama models: `docker exec askmydocs-ollama ollama list`
3. Test API manually: `curl http://localhost:8000/docs`

## Extending Tests

To add new test cases:

1. Add test methods following the `test_*` naming convention
2. Use appropriate assertions for validation
3. Include both positive and negative test scenarios
4. Add descriptive print statements for test progress
5. Update this README with new test descriptions

## Integration with CI/CD

These tests are designed to be run in automated environments:

- Exit codes: 0 for success, 1 for failure
- Structured output for parsing
- Docker-based execution for consistency
- Configurable timeouts and retry logic
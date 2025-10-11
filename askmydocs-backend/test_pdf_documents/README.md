# 📄 PDF Document Testing Suite

This directory contains comprehensive testing tools for PDF document processing in the AskMyDocs application.

## 📁 Directory Structure

```
test_pdf_documents/           # PDF files for testing
├── sample_document.pdf       # Basic test document
├── technology_overview.pdf   # Technology topics
├── business_strategy.pdf     # Business and management content  
├── research_methodology.pdf  # Scientific research content
└── (any additional PDF files)

test_pdf_processing_enhanced.py   # Enhanced PDF processor
create_multiple_pdfs.py          # Script to create sample PDFs
```

## 🚀 How It Works

The enhanced PDF testing system automatically:

1. **Discovers** all PDF files in the `test_pdf_documents/` folder
2. **Extracts** text content from each PDF using PyPDF2
3. **Adds** each PDF's content to the API as searchable documents
4. **Tests** querying functionality with various questions
5. **Validates** the complete PDF-to-query workflow

## 🧪 Running PDF Tests

### Quick Test (Single Command)
```bash
# Run comprehensive PDF test suite
docker exec askmydocs-backend python test_pdf_processing_enhanced.py
```

### Manual Testing Steps
```bash
# 1. Create additional test PDFs (optional)
docker exec askmydocs-backend python create_multiple_pdfs.py

# 2. Run the enhanced PDF processor
docker exec askmydocs-backend python test_pdf_processing_enhanced.py

# 3. Test specific queries
curl -X POST "http://localhost:8000/chat/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What technologies are mentioned in the documents?"}'
```

## 📝 Adding Your Own PDF Files

To test with your own PDF files:

1. **Copy PDF files** to the `test_pdf_documents/` folder:
   ```bash
   cp your_document.pdf /home/pkmittal/MyDemo/AskMyDocs/askmydocs-backend/test_pdf_documents/
   ```

2. **Run the processor** - it will automatically discover and process all PDFs:
   ```bash
   docker exec askmydocs-backend python test_pdf_processing_enhanced.py
   ```

3. **Query the content** using the API:
   ```bash
   curl -X POST "http://localhost:8000/chat/query" \
        -H "Content-Type: application/json" \
        -d '{"query": "Your question about the PDF content"}'
   ```

## 🔍 Test Coverage

### PDF Processing Tests
- ✅ **Auto-discovery** of PDF files in folder
- ✅ **Text extraction** from single and multi-page PDFs
- ✅ **Metadata extraction** (pages, file size, content length)
- ✅ **Error handling** for corrupted or unreadable PDFs
- ✅ **API integration** for document addition

### Query Tests  
- ✅ **Generic queries** that work with any document
- ✅ **Content-specific queries** based on PDF topics
- ✅ **Multi-document retrieval** from PDF collection
- ✅ **Response validation** (answer, sources, LLM used)

### Supported PDF Types
- ✅ **Text-based PDFs** (created from documents, reports)
- ✅ **Multi-page documents** 
- ✅ **Various content types** (technical, business, research)
- ⚠️  **Scanned PDFs** (OCR not implemented - text extraction may fail)

## 📊 Sample Test Results

```
🔍 Discovered 4 PDF files in /app/test_pdf_documents
   📄 sample_document.pdf (2270 bytes)
   📄 business_strategy.pdf (2278 bytes)  
   📄 technology_overview.pdf (2300 bytes)
   📄 research_methodology.pdf (2332 bytes)

📊 Processing Summary:
   Total PDFs found: 4
   Successfully processed: 4
   Documents added to API: 4

✅ Total: 4 PDF documents successfully processed
✅ PDF text extraction working
✅ API document addition working  
✅ Query processing working
✅ End-to-end PDF workflow validated
```

## 🛠️ Customization

### Adding New PDF Types
1. Add your PDF files to `test_pdf_documents/`
2. The system automatically processes all `.pdf` files
3. No code changes required for new documents

### Custom Query Tests
Edit `test_pdf_processing_enhanced.py` and modify the `test_queries` list:
```python
test_queries = [
    "Your custom question 1",
    "Your custom question 2",
    "Domain-specific queries",
]
```

### Different PDF Sources
The system can handle PDFs from various sources:
- **Generated PDFs** (from Word, Google Docs, etc.)
- **Downloaded documents** (research papers, reports)
- **Created PDFs** (using reportlab, as in our samples)
- **Exported content** (presentations, web pages)

## 🚨 Troubleshooting

### Common Issues

**PDF not found:**
- Check file is in `test_pdf_documents/` folder
- Verify file permissions and accessibility

**Text extraction fails:**
- PDF might be image-based (scanned document)
- Try with text-based PDF instead
- Check PDF is not password-protected

**Query returns no results:**
- Verify documents were added successfully to API
- Try more general queries
- Check embedding system is working

**Timeout errors:**
- Increase timeout in request calls
- Check if Ollama service is responsive
- Try simpler queries first

## 🔧 Technical Details

### Dependencies
- **PyPDF2**: PDF text extraction
- **requests**: API communication  
- **reportlab**: PDF generation (for samples)
- **pathlib/glob**: File discovery
- **os**: File system operations

### API Integration
- Uses `/chat/add_document` endpoint for PDF content
- Uses `/chat/query` endpoint for questions
- Handles timeouts and error responses
- Validates API response format

This testing suite ensures that the PDF processing functionality works reliably with any PDF documents you want to test!
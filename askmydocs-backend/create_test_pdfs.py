#!/usr/bin/env python3
"""
Script to create sample PDF files for testing
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def create_sample_pdf():
    """Create a sample PDF file for testing"""
    
    # Create the PDF file
    pdf_path = "/app/test_pdf_documents/sample_document.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    
    # Get sample styles
    styles = getSampleStyleSheet()
    
    # Content for the PDF
    story = []
    
    # Title
    title = Paragraph("Sample Test Document", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Content
    content = """
    This is a sample PDF document created for testing the AskMyDocs application.
    
    The document contains information about various topics including:
    
    1. Artificial Intelligence and Machine Learning
    2. Programming languages like Python
    3. Web frameworks such as FastAPI
    4. Database technologies
    5. Cloud computing concepts
    
    This document should be processed by the embedding system and made searchable
    through the query interface. The text extraction and embedding functionality
    will be tested using this document.
    
    Key testing scenarios include:
    - Document upload and processing
    - Text extraction from PDF format
    - Embedding generation for semantic search
    - Query processing and response generation
    - Retrieval of relevant document sections
    
    The document serves as a comprehensive test case for the entire RAG
    (Retrieval Augmented Generation) pipeline implemented in the AskMyDocs
    application.
    """
    
    for paragraph in content.split('\n\n'):
        if paragraph.strip():
            p = Paragraph(paragraph.strip(), styles['Normal'])
            story.append(p)
            story.append(Spacer(1, 12))
    
    # Build PDF
    doc.build(story)
    print(f"Created PDF: {pdf_path}")

if __name__ == "__main__":
    create_sample_pdf()
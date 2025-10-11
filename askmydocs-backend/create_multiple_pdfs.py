#!/usr/bin/env python3
"""
Create multiple sample PDF files for comprehensive testing
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def create_multiple_test_pdfs():
    """Create multiple PDF files with different content for testing"""
    
    pdf_dir = "/app/test_pdf_documents"
    os.makedirs(pdf_dir, exist_ok=True)
    
    styles = getSampleStyleSheet()
    
    # PDF 1: Technology Overview
    print("📝 Creating Technology Overview PDF...")
    doc1 = SimpleDocTemplate(f"{pdf_dir}/technology_overview.pdf", pagesize=letter)
    story1 = []
    
    title1 = Paragraph("Technology Overview Document", styles['Title'])
    story1.append(title1)
    story1.append(Spacer(1, 12))
    
    content1 = """
    Modern Technology Landscape
    
    This document provides an overview of current technology trends and developments.
    
    Artificial Intelligence:
    - Machine Learning algorithms are revolutionizing data analysis
    - Natural Language Processing enables human-computer interaction
    - Computer Vision applications in healthcare and autonomous vehicles
    
    Web Development:
    - Frontend frameworks like React, Vue, and Angular
    - Backend technologies including Node.js, Python Flask/Django
    - Database systems: SQL (PostgreSQL, MySQL) and NoSQL (MongoDB, Redis)
    
    Cloud Computing:
    - Infrastructure as a Service (IaaS)
    - Platform as a Service (PaaS)
    - Software as a Service (SaaS)
    - Major providers: AWS, Google Cloud, Microsoft Azure
    
    DevOps Practices:
    - Continuous Integration and Continuous Deployment (CI/CD)
    - Containerization with Docker and Kubernetes
    - Infrastructure as Code (IaC)
    - Monitoring and logging systems
    """
    
    for paragraph in content1.split('\n\n'):
        if paragraph.strip():
            p = Paragraph(paragraph.strip(), styles['Normal'])
            story1.append(p)
            story1.append(Spacer(1, 12))
    
    doc1.build(story1)
    print("✅ Created technology_overview.pdf")
    
    # PDF 2: Business Guide
    print("📝 Creating Business Strategy PDF...")
    doc2 = SimpleDocTemplate(f"{pdf_dir}/business_strategy.pdf", pagesize=letter)
    story2 = []
    
    title2 = Paragraph("Business Strategy and Management", styles['Title'])
    story2.append(title2)
    story2.append(Spacer(1, 12))
    
    content2 = """
    Strategic Business Planning Guide
    
    This document outlines key principles for effective business strategy and management.
    
    Strategic Planning Process:
    1. Market Analysis and Competitive Research
    2. SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)
    3. Goal Setting and Objective Definition
    4. Resource Allocation and Budget Planning
    5. Implementation Timeline and Milestones
    
    Digital Transformation:
    - Adopting cloud-based solutions
    - Implementing data analytics for decision making
    - Automating business processes
    - Enhancing customer experience through technology
    
    Team Management:
    - Agile methodologies and Scrum frameworks
    - Remote work best practices
    - Performance management systems
    - Employee development and training programs
    
    Financial Management:
    - Cash flow analysis and forecasting
    - Investment evaluation criteria
    - Risk assessment and mitigation strategies
    - Key Performance Indicators (KPIs) tracking
    """
    
    for paragraph in content2.split('\n\n'):
        if paragraph.strip():
            p = Paragraph(paragraph.strip(), styles['Normal'])
            story2.append(p)
            story2.append(Spacer(1, 12))
    
    doc2.build(story2)
    print("✅ Created business_strategy.pdf")
    
    # PDF 3: Scientific Research
    print("📝 Creating Scientific Research PDF...")
    doc3 = SimpleDocTemplate(f"{pdf_dir}/research_methodology.pdf", pagesize=letter)
    story3 = []
    
    title3 = Paragraph("Research Methodology and Data Analysis", styles['Title'])
    story3.append(title3)
    story3.append(Spacer(1, 12))
    
    content3 = """
    Scientific Research Methods and Data Analysis
    
    This document covers fundamental principles of scientific research and data analysis techniques.
    
    Research Design:
    - Experimental vs. Observational Studies
    - Quantitative and Qualitative Research Methods
    - Sample Selection and Statistical Power
    - Control Groups and Variable Management
    
    Data Collection Methods:
    - Surveys and Questionnaires
    - Interviews and Focus Groups
    - Laboratory Experiments
    - Field Studies and Natural Observations
    
    Statistical Analysis:
    - Descriptive Statistics (Mean, Median, Mode, Standard Deviation)
    - Inferential Statistics and Hypothesis Testing
    - Correlation and Regression Analysis
    - ANOVA and Chi-Square Tests
    
    Research Tools and Software:
    - Statistical Software: R, SPSS, SAS
    - Data Visualization: Tableau, Power BI, Python Matplotlib
    - Survey Platforms: Qualtrics, SurveyMonkey
    - Reference Management: Zotero, Mendeley
    
    Ethical Considerations:
    - Informed Consent and Participant Rights
    - Data Privacy and Confidentiality
    - Research Integrity and Reproducibility
    - Peer Review Process
    """
    
    for paragraph in content3.split('\n\n'):
        if paragraph.strip():
            p = Paragraph(paragraph.strip(), styles['Normal'])
            story3.append(p)
            story3.append(Spacer(1, 12))
    
    doc3.build(story3)
    print("✅ Created research_methodology.pdf")
    
    print(f"\n🎉 Created 3 test PDF files in {pdf_dir}")

if __name__ == "__main__":
    create_multiple_test_pdfs()
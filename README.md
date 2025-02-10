# AI Data Extraction & Processing Prototype

This repository contains a prototype AI application designed to extract, process, and standardize data from unstructured sources such as PDF files and web pages. The project evaluates both open-source libraries and enterprise-grade solutions to determine their feasibility, performance, and integration capabilities.

## Description

This prototype demonstrates how to:
- Extract data from PDFs using Python tools (PyPDF2, pdfplumber) and enterprise services (Microsoft Document Intelligence).
- Scrape web pages using libraries like BeautifulSoup alongside enterprise capabilities for content processing.
- Standardize document content into Markdown format with tools such as Docling and MarkItDown.
- Organize processed files (including links to images) in AWS S3 buckets using a structured naming convention and metadata tagging.
- Expose RESTful API endpoints with FastAPI and provide a user-friendly interface via a Streamlit application.

The goal is to evaluate multiple products and workflows to select the best tools for scalable and accurate data processing.


## Installation & Setup

1. **Clone the Repository:**
git clone https://github.com/Tanmay6461/PyTract.git
cd ai-data-extraction-prototype

2. **Set Up Virtual Environment & Install Dependencies:**
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
pip install -r requirements.txt

3. **Configuration (.env File)**
Create a `.env` file at the root of the project and add your environment-specific configurations.

## Usage
- **Run the API Server:**
uvicorn app:app --reload

- **Start the Frontend Application:**
streamlit run frontend/streamlit-app.py




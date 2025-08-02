import PyPDF2
from docx import Document
import os

def load_document(file_path):
    """Load PDF or DOCX file content"""
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
            
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    
    else:
        raise ValueError("Unsupported file format")
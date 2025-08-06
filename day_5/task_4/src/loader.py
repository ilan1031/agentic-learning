from PyPDF2 import PdfReader

def load_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

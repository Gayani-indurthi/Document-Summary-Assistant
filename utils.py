import PyPDF2
import pytesseract
from PIL import Image
import io
import os

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    text = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_image(file_path):
    """Extract text from an image file using OCR."""
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text(file_path):
    """Extract text from either PDF or image file."""
    _, ext = os.path.splitext(file_path)
    if ext.lower() == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext.lower() in ['.jpg', '.jpeg', '.png']:
        return extract_text_from_image(file_path)
    else:
        raise ValueError("Unsupported file type. Only PDF, JPG, and PNG are supported.")

import io
import docx
from pypdf import PdfReader
from fastapi import UploadFile


def extract_text(file: UploadFile):
    """Extracts text from a .pdf or .docx file."""

    file_extension = file.filename.split('.')[-1].lower()

    if file_extension == "pdf":
        pdf_reader = PdfReader(io.BytesIO(file.file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text

    elif file_extension == "docx":
        doc = docx.Document(io.BytesIO(file.file.read()))
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text

    else:
        return None
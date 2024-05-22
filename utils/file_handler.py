import fitz  # PyMuPDF
import docx
from PIL import Image
import pytesseract
import streamlit as st


def handle_file_upload(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file)
    elif uploaded_file.type in ["image/jpeg", "image/png"]:
        return extract_text_from_image(uploaded_file)
    else:
        st.error("Unsupported file type.")
        return None, None


def extract_text_from_pdf(pdf_file):
    pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    return text


def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text_from_image(image_file):
    image = Image.open(image_file)
    return pytesseract.image_to_string(image)

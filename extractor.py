import os
from PyPDF2 import PdfReader
from docx import Document


def get_filename(file_obj_or_path):
    """Get filename whether it's a path string or an uploaded file object."""
    if isinstance(file_obj_or_path, str):
        return file_obj_or_path
    return file_obj_or_path.name  # Streamlit's UploadedFile has a .name attribute


def extract_text_from_pdf(file_obj_or_path):
    text = ""
    reader = PdfReader(file_obj_or_path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def extract_text_from_docx(file_obj_or_path):
    doc = Document(file_obj_or_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def extract_text_from_txt(file_obj_or_path):
    if isinstance(file_obj_or_path, str):
        with open(file_obj_or_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        # Uploaded file object: read bytes, then decode
        return file_obj_or_path.read().decode("utf-8")


def extract_text(file_obj_or_path):
    """
    Works with BOTH a disk file path (string) AND a Streamlit
    uploaded file object. Detects type by filename extension.
    """
    filename = get_filename(file_obj_or_path)
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_obj_or_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_obj_or_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_obj_or_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


if __name__ == "__main__":
    test_path = "sample_data/resume1.txt"
    if os.path.exists(test_path):
        text = extract_text(test_path)
        print(text[:500])
    else:
        print(f"File not found: {test_path}")
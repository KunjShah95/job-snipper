"""
Helpers for] saving uploaded files, detecting types, creating directories, and safe filenames.
"""

import os
import pathlib
import mimetypes
from typing import Tuple

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "data/resumes")
REPORT_DIR = os.getenv("REPORT_DIR", "data/reports")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

def safe_filename(filename: str) -> str:
    """Return a safe filename stripped of directory parts."""
    return pathlib.Path(filename).name

def save_uploaded_file(uploaded_file, dest_dir: str = UPLOAD_DIR) -> str:
    """
    Save a Streamlit/InMemory uploaded file-like object to disk.
    uploaded_file must support .read() and .name property.
    Returns saved file path.
    """
    name = safe_filename(getattr(uploaded_file, "name", "uploaded_file"))
    out_path = os.path.join(dest_dir, name)
    with open(out_path, "wb") as f:
        f.write(uploaded_file.read())
    return out_path

def detect_file_type(file_path: str) -> Tuple[str, str]:
    """
    Return (mimetype, simple_type) where simple_type is 'pdf'/'docx'/'other'
    """
    mime, _ = mimetypes.guess_type(file_path)
    mime = mime or ""
    ext = os.path.splitext(file_path)[1].lower()
    if mime == "application/pdf" or ext == ".pdf":
        return mime or "application/pdf", "pdf"
    if mime in ("application/vnd.openxmlformats-officedocument.wordprocessingml.document",) or ext == ".docx":
        return mime or "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "docx"
    if ext == ".txt":
        return mime or "text/plain", "txt"
    if ext in [".doc", ".rtf"]:
        return mime or "application/msword", "doc"
    return mime or "application/octet-stream", "other"

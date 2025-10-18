from services.docx_parser import parse_document
from services.resume_parser import parse_resume_to_json


def parse_resume(file_path, file_type):
    """
    Parse a resume file into structured JSON.
    Supports PDF, DOCX, and OCR for scanned PDFs.
    """
    try:
        # Use the unified document parser which handles PDF, DOCX, txt and
        # extracts images and runs OCR where appropriate. It returns (text, manifest).
        text, manifest = parse_document(file_path)

        if not text or not text.strip():
            print("No text extracted from document; manifest:", manifest)

        parsed_resume = parse_resume_to_json(text)
        # include manifest for debugging and UI diagnostics
        parsed_resume["_manifest"] = manifest
        return parsed_resume
    except Exception as e:
        print(f"Parser agent failed: {e}")
        return {"skills": [], "education": [], "experience": [], "raw_text": "", "_manifest": {"errors": [str(e)]}}

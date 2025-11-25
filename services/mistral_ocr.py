"""
Mistral OCR stub

This module used to call an external Mistral OCR service. Mistral support
was intentionally removed; this stub keeps the import surface so existing
call sites don't crash immediately. If called, it returns an empty string
and logs an informational message.
"""

import logging
import os
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

# Backend selection via environment variable. Options: 'tesseract' (default), 'google_vision'
OCR_BACKEND = os.getenv("OCR_BACKEND", "tesseract").lower()


class MistralOCR:
    """Compatibility wrapper that provides OCR using either local Tesseract
    (via pytesseract) or Google Cloud Vision. The class name is preserved to
    avoid changing imports elsewhere in the codebase.

    Behavior:
      - If OCR_BACKEND=tesseract and pytesseract/Pillow are installed, use them.
      - If OCR_BACKEND=google_vision and google-cloud-vision is installed and
        credentials are configured, use the Vision API.
      - If dependencies are missing or an error occurs, returns an empty string
        and logs a warning.
    """

    def __init__(self, backend: str | None = None, *args, **kwargs):
        self.backend = (backend or OCR_BACKEND).lower()
        log.info("Initializing OCR backend: %s", self.backend)

        # Lazy imports
        self._has_pytesseract = False
        self._has_pillow = False
        self._has_fitz = False
        self._has_gvision = False

        try:
            import PIL.Image as PILImage  # type: ignore

            self._has_pillow = True
            self._PILImage = PILImage
        except Exception:
            self._PILImage = None

        try:
            import pytesseract  # type: ignore

            self._has_pytesseract = True
            self._pytesseract = pytesseract
        except Exception:
            self._pytesseract = None

        try:
            import fitz  # PyMuPDF

            self._has_fitz = True
            self._fitz = fitz
        except Exception:
            self._fitz = None

        try:
            # google cloud vision
            from google.cloud import vision  # type: ignore

            self._has_gvision = True
            self._vision = vision
        except Exception:
            self._vision = None

    def _ocr_with_tesseract_from_image(self, image) -> str:
        if not (self._has_pytesseract and self._has_pillow):
            log.debug("pytesseract or Pillow not available")
            return ""
        try:
            text = self._pytesseract.image_to_string(image)
            return text or ""
        except Exception as e:
            log.warning("Tesseract OCR failed: %s", e)
            return ""

    def _ocr_with_gvision_bytes(self, image_bytes: bytes) -> str:
        if not self._has_gvision:
            log.debug("google-cloud-vision not available")
            return ""
        try:
            client = self._vision.ImageAnnotatorClient()
            image = self._vision.Image(content=image_bytes)
            response = client.text_detection(image=image)
            if response.error.message:
                log.warning("Google Vision API error: %s", response.error.message)
                return ""
            texts = response.text_annotations
            if texts:
                return texts[0].description or ""
            return ""
        except Exception as e:
            log.warning("Google Vision OCR failed: %s", e)
            return ""

    def extract_text(self, file_path: str) -> str:
        """Extract text from a file path. Supports images and PDFs.

        For PDFs, if PyMuPDF (fitz) is available we render pages to images and
        OCR each page. For images we use the selected backend directly.
        """
        if not os.path.exists(file_path):
            log.warning("OCR file does not exist: %s", file_path)
            return ""

        ext = os.path.splitext(file_path)[1].lower()

        # Helper to OCR raw bytes via chosen backend
        def ocr_bytes(b: bytes) -> str:
            if self.backend == "google_vision":
                return self._ocr_with_gvision_bytes(b)
            # default to tesseract
            if self._has_pillow:
                try:
                    img = self._PILImage.open(BytesIO(b))
                    return self._ocr_with_tesseract_from_image(img)
                except Exception as e:
                    log.warning("Pillow failed to open bytes: %s", e)
                    return ""
            return ""

        # If PDF, try to render pages to images using fitz (PyMuPDF)
        if ext == ".pdf" and self._has_fitz:
            try:
                doc = self._fitz.open(file_path)
                page_texts = []
                for p in doc:
                    try:
                        pix = p.get_pixmap()
                        img_bytes = pix.tobytes("png")
                        text = ocr_bytes(img_bytes)
                        if text:
                            page_texts.append(text)
                    except Exception as e:
                        log.debug("Failed rendering page for OCR: %s", e)
                        continue
                return "\n\n".join(page_texts)
            except Exception as e:
                log.warning("PDF OCR via fitz failed: %s", e)

        # For images or fallback, read bytes and OCR
        try:
            with open(file_path, "rb") as f:
                b = f.read()
            return ocr_bytes(b)
        except Exception as e:
            log.warning("OCR read failed for %s: %s", file_path, e)
            return ""

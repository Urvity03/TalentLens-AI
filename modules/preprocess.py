"""Text extraction, normalization, and section detection utilities."""

from pathlib import Path
import re

import fitz
from docx import Document

from modules.config import SECTION_NAMES, SECTION_PATTERN


def extract_text_from_pdf(file_path: str | Path) -> str:
    """Extract readable text from a PDF file.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Raw text extracted from all PDF pages.
    """
    with fitz.open(file_path) as document:
        return "\n".join(page.get_text("text") for page in document)


def extract_text_from_docx(file_path: str | Path) -> str:
    """Extract readable text from a DOCX file.

    Args:
        file_path: Path to the DOCX file.

    Returns:
        Raw text extracted from document paragraphs.
    """
    document = Document(file_path)
    return "\n".join(paragraph.text for paragraph in document.paragraphs)


def normalize_text(text: str) -> str:
    """Normalize whitespace while preserving paragraph breaks.

    Args:
        text: Raw extracted text.

    Returns:
        Clean text with consistent spacing and line breaks.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(lines).strip()


def detect_resume_sections(text: str) -> dict[str, str]:
    """Detect common resume sections in normalized text.

    Args:
        text: Resume text to inspect.

    Returns:
        Mapping of section names to section content. Missing sections are empty.
    """
    sections = {name: "" for name in SECTION_NAMES}
    matches = list(SECTION_PATTERN.finditer(text))

    for index, match in enumerate(matches):
        section_name = match.group(1).strip().title()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[section_name] = text[start:end].strip()

    return sections


def preprocess_file(file_path: str | Path) -> dict[str, str | dict[str, str]]:
    """Extract, normalize, and section resume text from a supported file.

    Args:
        file_path: Path to a PDF or DOCX file.

    Returns:
        Dictionary containing normalized text and detected sections.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not supported.
        ValueError: If no readable text is extracted.
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    extractors = {
        ".pdf": extract_text_from_pdf,
        ".docx": extract_text_from_docx,
    }

    extractor = extractors.get(path.suffix.lower())
    if extractor is None:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    text = normalize_text(extractor(path))
    if not text:
        raise ValueError(f"No readable text extracted from: {path}")

    return {"text": text, "sections": detect_resume_sections(text)}

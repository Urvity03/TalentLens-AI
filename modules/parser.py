"""Parse preprocessed resume data into a Resume object."""

from pathlib import Path
import re

from modules.models import (
    Certification,
    ContactInfo,
    Education,
    Experience,
    Project,
    Resume,
)
from modules.preprocess import preprocess_file
from modules.skill_extractor import extract_skills


EMAIL_PATTERN = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
PHONE_PATTERN = re.compile(r"\+?\d[\d\s\-()]{8,}\d")


def _extract_contact(text: str) -> ContactInfo:
    """Extract candidate contact information."""

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    email = EMAIL_PATTERN.search(text)
    phone = PHONE_PATTERN.search(text)

    return ContactInfo(
        name=lines[0] if lines else None,
        email=email.group() if email else None,
        phone=phone.group() if phone else None,
        linkedin=next((l for l in lines if "linkedin.com" in l.lower()), None),
        github=next((l for l in lines if "github.com" in l.lower()), None),
    )


def _wrap(text: str, model):
    """Wrap a resume section into its corresponding dataclass."""

    return [model(description=text.strip())] if text.strip() else []


def parse_resume(file_path: str | Path) -> Resume:
    """Parse a resume into a Resume object."""

    data = preprocess_file(file_path)
    sections = data["sections"]

    return Resume(
        contact=_extract_contact(data["text"]),
        summary=sections.get("Summary", ""),
        skills=extract_skills(sections.get("Skills", "")),
        experience=_wrap(sections.get("Experience", ""), Experience),
        education=_wrap(sections.get("Education", ""), Education),
        projects=_wrap(sections.get("Projects", ""), Project),
        certifications=_wrap(
            sections.get("Certifications", ""),
            Certification,
        ),
    )
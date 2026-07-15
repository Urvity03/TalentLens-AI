"""Parse preprocessed resume data into a Resume object."""

from pathlib import Path
import re

from modules.config import SUPPORTED_SKILLS
from modules.models import (
    Certification,
    ContactInfo,
    Education,
    Experience,
    Project,
    Resume,
    Skill,
)
from modules.preprocess import preprocess_file


EMAIL_PATTERN = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
PHONE_PATTERN = re.compile(r"\+?\d[\d\s\-()]{8,}\d")


def _extract_contact(text: str) -> ContactInfo:
    """Extract basic contact information."""

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    email = EMAIL_PATTERN.search(text)
    phone = PHONE_PATTERN.search(text)

    linkedin = next((line for line in lines if "linkedin.com" in line.lower()), None)
    github = next((line for line in lines if "github.com" in line.lower()), None)

    return ContactInfo(
        name=lines[0] if lines else None,
        email=email.group() if email else None,
        phone=phone.group() if phone else None,
        linkedin=linkedin,
        github=github,
    )


def _extract_skills(text: str) -> list[Skill]:
    """Match resume text against supported skills."""

    text = text.lower()

    return [
        Skill(name=skill)
        for skill in SUPPORTED_SKILLS
        if skill.lower() in text
    ]


def _wrap(section: str, model):
    """Wrap raw section text into dataclass objects."""

    return [model(description=section.strip())] if section.strip() else []


def parse_resume(file_path: str | Path) -> Resume:
    """Parse a resume file into a Resume object."""

    data = preprocess_file(file_path)

    text = data["text"]
    sections = data["sections"]

    return Resume(
        contact=_extract_contact(text),
        summary=sections.get("Summary", ""),
        skills=_extract_skills(sections.get("Skills", "")),
        experience=_wrap(sections.get("Experience", ""), Experience),
        education=_wrap(sections.get("Education", ""), Education),
        projects=_wrap(sections.get("Projects", ""), Project),
        certifications=_wrap(
            sections.get("Certifications", ""),
            Certification,
        ),
    )
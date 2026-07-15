"""Project configuration values for TalentLens-AI."""

import re


SECTION_NAMES = (
    "Summary",
    "Skills",
    "Experience",
    "Education",
    "Projects",
    "Certifications",
)

SECTION_PATTERN = re.compile(
    r"(?im)^\s*(summary|skills|experience|education|projects|certifications)\s*:?\s*$"
)

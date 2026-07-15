"""Extract supported skills from text."""

import re

from modules.config import SUPPORTED_SKILLS
from modules.models import Skill


def extract_skills(text: str) -> list[Skill]:
    """Return supported skills found in text."""

    text = text.lower()

    return [
        Skill(name=skill)
        for skill in SUPPORTED_SKILLS
        if re.search(rf"\b{re.escape(skill.lower())}\b", text)
    ]
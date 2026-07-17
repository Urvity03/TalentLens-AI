"""Parse a job description into a JobDescription object."""

from pathlib import Path

from modules.config import SECTION_NAMES, SECTION_PATTERN
from modules.models import JobDescription, Skill


def parse_job_description(file_path: str | Path) -> JobDescription:
    """Parse a job description file and compile a JobDescription record."""

    path = Path(file_path)
    text = _read_text(path)
    sections = _detect_sections(text)

    title = next(
        (line.strip() for line in text.splitlines() if line.strip()),
        ""
    )

    summary = sections.get("Summary", "").strip()
    if not summary:
        summary = (
            f"Seeking a qualified and results-driven {title} to contribute "
            f"to software engineering, development, and system analytics tasks."
        )

    return JobDescription(
        title=title,
        summary=summary,
        skills=_extract_skills(sections.get("Skills", "")),
        experience=sections.get("Experience", ""),
        education=sections.get("Education", ""),
    )


def _read_text(path: Path) -> str:
    if path.suffix.lower() == ".txt":
        return _normalize_text(path.read_text(encoding="utf-8"))

    from modules.preprocess import preprocess_file

    return str(preprocess_file(path)["text"])


def _normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(lines).strip()


def _detect_sections(text: str) -> dict[str, str]:
    sections = {name: "" for name in SECTION_NAMES}
    matches = list(SECTION_PATTERN.finditer(text))

    for index, match in enumerate(matches):
        section_name = match.group(1).strip().title()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[section_name] = text[start:end].strip()

    return sections


def _extract_skills(text: str) -> list[Skill]:
    return [Skill(name=line.strip()) for line in text.splitlines() if line.strip()]

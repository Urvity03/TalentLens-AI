"""Resume quality score calculation."""

from modules.models import Resume


def calculate_resume_quality(resume: Resume) -> float:
    """Calculate the quality score of a resume out of 100.

    Args:
        resume: The Resume object to score.

    Returns:
        The final score rounded to 2 decimal places.
    """
    score = 0.0

    if resume.contact.name:
        score += 10.0
    if resume.contact.email:
        score += 10.0
    if resume.contact.phone:
        score += 10.0
    if resume.summary and resume.summary.strip():
        score += 10.0
    if resume.skills:
        score += 20.0
    if resume.experience:
        score += 15.0
    if resume.education:
        score += 15.0
    if resume.projects:
        score += 10.0

    return round(score, 2)

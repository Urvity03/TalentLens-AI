"""Skill intelligence and matching calculation."""

from modules.models import JobDescription, Resume, SkillIntelligence


def analyze_skill_match(
    resume: Resume,
    job_description: JobDescription,
) -> SkillIntelligence:
    """Analyze skill match between resume and job description.

    Args:
        resume: The Resume object.
        job_description: The JobDescription object.

    Returns:
        A SkillIntelligence object with matched/missing lists and match percentage.
    """
    if not job_description.skills:
        return SkillIntelligence()

    resume_skills = {s.name.lower() for s in resume.skills}

    matched: list[str] = []
    missing: list[str] = []

    for skill in job_description.skills:
        if skill.name.lower() in resume_skills:
            matched.append(skill.name)
        else:
            missing.append(skill.name)

    match_percentage = round((len(matched) / len(job_description.skills)) * 100, 2)

    return SkillIntelligence(
        matched=matched,
        missing=missing,
        match_percentage=match_percentage,
    )

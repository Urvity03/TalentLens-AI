"""Adaptive Hiring Readiness Index (AHRI) calculation."""

from modules.config import (
    AHRI_GRADES,
    AHRI_MAX_BONUS,
    AHRI_MAX_PENALTY,
    AHRI_SKILL_BONUS,
    AHRI_SKILL_PENALTY,
    SIMILARITY_WEIGHTS,
)
from modules.models import (
    AHRIResult,
    JobDescription,
    Resume,
    SimilarityResult,
)


def calculate_ahri(
    resume: Resume,
    job_description: JobDescription,
    similarity: SimilarityResult,
) -> AHRIResult:
    """Calculate the Adaptive Hiring Readiness Index (AHRI) score and grade.

    Args:
        resume: The parsed resume object.
        job_description: The parsed job description object.
        similarity: The semantic similarity results between resume and JD.

    Returns:
        An AHRIResult containing the score, grade, strengths, missing skills,
        and recommendation.
    """
    resume_skills = {s.name.lower() for s in resume.skills}

    strengths: list[str] = []
    missing_skills: list[str] = []

    for skill in job_description.skills:
        if skill.name.lower() in resume_skills:
            strengths.append(skill.name)
        else:
            missing_skills.append(skill.name)

    base_score = (
        similarity.summary * SIMILARITY_WEIGHTS["summary"]
        + similarity.skills * SIMILARITY_WEIGHTS["skills"]
        + similarity.experience * SIMILARITY_WEIGHTS["experience"]
    )

    bonus = min(
        len(strengths) * AHRI_SKILL_BONUS,
        AHRI_MAX_BONUS,
    )
    penalty = min(
        len(missing_skills) * AHRI_SKILL_PENALTY,
        AHRI_MAX_PENALTY,
    )

    score = round(max(0.0, min(base_score + bonus - penalty, 100.0)), 2)
    grade = next(g for limit, g in AHRI_GRADES if score >= limit)

    recommendation = (
        "Learn the following skills to improve your hiring readiness: "
        f"{', '.join(missing_skills)}"
        if missing_skills
        else "Excellent match for this position."
    )

    return AHRIResult(
        score=score,
        grade=grade,
        strengths=strengths,
        missing_skills=missing_skills,
        recommendation=recommendation,
    )

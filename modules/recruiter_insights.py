"""Recruiter insights generation."""

from modules.models import (
    AHRIResult,
    PotentialPrediction,
    RecruiterInsights,
    SkillIntelligence,
)


def generate_recruiter_insights(
    ahri: AHRIResult,
    skill_intelligence: SkillIntelligence,
    quality_score: float,
    prediction: PotentialPrediction,
) -> RecruiterInsights:
    """Generate recruiter insights containing strengths, concerns, and a recommendation.

    Args:
        ahri: The computed AHRI result.
        skill_intelligence: The computed skill intelligence match results.
        quality_score: The computed resume quality score.
        prediction: The computed potential prediction.

    Returns:
        A RecruiterInsights object.
    """
    strengths: list[str] = []
    concerns: list[str] = []

    if skill_intelligence.match_percentage >= 70.0:
        strengths.append("Strong skill match")
    if quality_score >= 80.0:
        strengths.append("High-quality resume")
    if ahri.score >= 80.0:
        strengths.append("High hiring readiness")
    if prediction.level in ["Outstanding", "Excellent"]:
        strengths.append(prediction.level)

    if skill_intelligence.missing:
        concerns.append("Several required skills are missing.")
    if quality_score < 70.0:
        concerns.append("Resume quality could be improved.")
    if prediction.level == "Needs Improvement":
        concerns.append("Candidate requires additional preparation.")

    recommendation = (
        "Hire recommended."
        if not concerns
        else "Consider after addressing identified skill gaps."
    )

    return RecruiterInsights(
        strengths=strengths,
        concerns=concerns,
        recommendation=recommendation,
    )

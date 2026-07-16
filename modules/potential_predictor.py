"""Potential predictor calculation."""

from modules.models import AHRIResult, PotentialPrediction, SkillIntelligence


def predict_candidate_potential(
    ahri: AHRIResult,
    skill_intelligence: SkillIntelligence,
    resume_quality: float,
) -> PotentialPrediction:
    """Predict a candidate's potential score and classification level.

    Args:
        ahri: The computed AHRI result.
        skill_intelligence: The computed skill intelligence match.
        resume_quality: The calculated resume quality score.

    Returns:
        A PotentialPrediction object containing the final score and level.
    """
    raw_score = (
        (ahri.score * 0.5)
        + (skill_intelligence.match_percentage * 0.3)
        + (resume_quality * 0.2)
    )
    score = round(max(0.0, min(raw_score, 100.0)), 2)

    if score >= 90.0:
        level = "Outstanding"
    elif score >= 80.0:
        level = "Excellent"
    elif score >= 70.0:
        level = "High"
    elif score >= 60.0:
        level = "Moderate"
    else:
        level = "Needs Improvement"

    return PotentialPrediction(score=score, level=level)

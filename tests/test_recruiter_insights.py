"""Test the recruiter insights module."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modules.models import (
    AHRIResult,
    PotentialPrediction,
    SkillIntelligence,
)
from modules.recruiter_insights import generate_recruiter_insights


def test_recruiter_insights_positive():
    """Test recruiter insights with no concerns (positive scenario)."""
    ahri = AHRIResult(score=85.0, grade="A")
    si = SkillIntelligence(matched=["Python", "SQL"], missing=[], match_percentage=100.0)
    quality_score = 90.0
    prediction = PotentialPrediction(score=88.0, level="Excellent")

    insights = generate_recruiter_insights(ahri, si, quality_score, prediction)

    # All strengths should be added
    assert "Strong skill match" in insights.strengths
    assert "High-quality resume" in insights.strengths
    assert "High hiring readiness" in insights.strengths
    assert "Excellent" in insights.strengths

    # No concerns should be generated
    assert len(insights.concerns) == 0
    assert insights.recommendation == "Hire recommended."
    print("[OK] Test recruiter insights positive passed")


def test_recruiter_insights_mixed():
    """Test recruiter insights with some concerns (mixed scenario)."""
    ahri = AHRIResult(score=60.0, grade="C")
    si = SkillIntelligence(matched=["Python"], missing=["SQL"], match_percentage=50.0)
    quality_score = 65.0
    prediction = PotentialPrediction(score=58.0, level="Needs Improvement")

    insights = generate_recruiter_insights(ahri, si, quality_score, prediction)

    # Check strengths (none should meet the threshold)
    assert len(insights.strengths) == 0

    # Concerns should be raised
    assert "Several required skills are missing." in insights.concerns
    assert "Resume quality could be improved." in insights.concerns
    assert "Candidate requires additional preparation." in insights.concerns

    assert insights.recommendation == "Consider after addressing identified skill gaps."
    print("[OK] Test recruiter insights mixed passed")


if __name__ == "__main__":
    print("Running recruiter insights module tests...\n")
    test_recruiter_insights_positive()
    test_recruiter_insights_mixed()
    print("\n[SUCCESS] All recruiter insights tests passed successfully!")

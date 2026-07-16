"""Test the potential predictor module."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modules.models import AHRIResult, SkillIntelligence
from modules.potential_predictor import predict_candidate_potential


def test_predict_outstanding():
    """Test Outstanding level (score >= 90.0)."""
    # 95 * 0.5 + 90 * 0.3 + 90 * 0.2 = 47.5 + 27 + 18 = 92.5
    ahri = AHRIResult(score=95.0, grade="A+")
    si = SkillIntelligence(match_percentage=90.0)
    result = predict_candidate_potential(ahri, si, 90.0)
    assert result.score == 92.5
    assert result.level == "Outstanding"
    print("[OK] Test Outstanding passed")


def test_predict_high():
    """Test High level (score 70 - 79.99)."""
    # 80 * 0.5 + 70 * 0.3 + 60 * 0.2 = 40 + 21 + 12 = 73.0
    ahri = AHRIResult(score=80.0, grade="A")
    si = SkillIntelligence(match_percentage=70.0)
    result = predict_candidate_potential(ahri, si, 60.0)
    assert result.score == 73.0
    assert result.level == "High"
    print("[OK] Test High passed")


def test_predict_moderate():
    """Test Moderate level (score 60 - 69.99)."""
    # 65 * 0.5 + 60 * 0.3 + 65 * 0.2 = 32.5 + 18 + 13 = 63.5
    ahri = AHRIResult(score=65.0, grade="C")
    si = SkillIntelligence(match_percentage=60.0)
    result = predict_candidate_potential(ahri, si, 65.0)
    assert result.score == 63.5
    assert result.level == "Moderate"
    print("[OK] Test Moderate passed")


def test_predict_needs_improvement():
    """Test Needs Improvement level (score < 60)."""
    # 50 * 0.5 + 40 * 0.3 + 50 * 0.2 = 25 + 12 + 10 = 47.0
    ahri = AHRIResult(score=50.0, grade="D")
    si = SkillIntelligence(match_percentage=40.0)
    result = predict_candidate_potential(ahri, si, 50.0)
    assert result.score == 47.0
    assert result.level == "Needs Improvement"
    print("[OK] Test Needs Improvement passed")


if __name__ == "__main__":
    print("Running potential predictor module tests...\n")
    test_predict_outstanding()
    test_predict_high()
    test_predict_moderate()
    test_predict_needs_improvement()
    print("\n[SUCCESS] All potential predictor tests passed successfully!")

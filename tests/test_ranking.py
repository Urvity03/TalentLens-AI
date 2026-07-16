"""Test the candidate ranking module."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modules.models import AHRIResult, Resume
from modules.ranking import rank_candidates


def test_rank_candidates():
    """Test that rank_candidates sorts candidates by AHRI score descending."""
    resume_a = Resume(summary="Candidate A")
    resume_b = Resume(summary="Candidate B")
    resume_c = Resume(summary="Candidate C")

    result_a = AHRIResult(score=75.0, grade="B")
    result_b = AHRIResult(score=92.5, grade="A+")
    result_c = AHRIResult(score=45.0, grade="F")

    candidates = [
        (resume_a, result_a),
        (resume_b, result_b),
        (resume_c, result_c),
    ]

    ranked = rank_candidates(candidates)

    assert len(ranked) == 3
    # Highest score first (92.5) -> (75.0) -> (45.0)
    assert ranked[0][1].score == 92.5
    assert ranked[0][0].summary == "Candidate B"

    assert ranked[1][1].score == 75.0
    assert ranked[1][0].summary == "Candidate A"

    assert ranked[2][1].score == 45.0
    assert ranked[2][0].summary == "Candidate C"

    print("[OK] Test rank candidates passed")


if __name__ == "__main__":
    print("Running ranking module tests...\n")
    test_rank_candidates()
    print("\n[SUCCESS] All ranking tests passed successfully!")

"""Test the resume quality score module."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modules.models import (
    ContactInfo,
    Education,
    Experience,
    Project,
    Resume,
    Skill,
)
from modules.quality_score import calculate_resume_quality


def test_quality_score_empty():
    """Test that an empty resume gets a score of 0.0."""
    resume = Resume()
    score = calculate_resume_quality(resume)
    assert score == 0.0
    print("[OK] Empty resume test passed")


def test_quality_score_full():
    """Test that a complete resume gets a score of 100.0."""
    resume = Resume(
        contact=ContactInfo(
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
        ),
        summary="A senior developer.",
        skills=[Skill(name="Python")],
        experience=[Experience(description="Built APIs")],
        education=[Education(description="B.S. Computer Science")],
        projects=[Project(description="Personal website")],
    )
    score = calculate_resume_quality(resume)
    assert score == 100.0
    print("[OK] Full resume test passed")


def test_quality_score_partial():
    """Test a partial resume with a subset of fields."""
    resume = Resume(
        contact=ContactInfo(
            name="Alice",
            email="alice@example.com",
        ),
        skills=[Skill(name="Java")],
        education=[Education(description="Self-taught")],
    )
    # name (10) + email (10) + skills (20) + education (15) = 55.0
    score = calculate_resume_quality(resume)
    assert score == 55.0
    print("[OK] Partial resume test passed")


if __name__ == "__main__":
    print("Running quality score module tests...\n")
    test_quality_score_empty()
    test_quality_score_full()
    test_quality_score_partial()
    print("\n[SUCCESS] All quality score tests passed successfully!")

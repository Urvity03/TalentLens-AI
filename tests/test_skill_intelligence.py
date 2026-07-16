"""Test the skill intelligence module."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modules.models import JobDescription, Resume, Skill
from modules.skill_intelligence import analyze_skill_match


def test_skill_match_no_jd_skills():
    """Test that a JobDescription with no skills returns 0.0 percentage."""
    resume = Resume(skills=[Skill(name="Python")])
    job_description = JobDescription()

    result = analyze_skill_match(resume, job_description)
    assert result.match_percentage == 0.0
    assert result.matched == []
    assert result.missing == []
    print("[OK] Test no JD skills passed")


def test_skill_match_partial():
    """Test partial match and case-insensitivity preserving original names."""
    resume = Resume(skills=[Skill(name="python"), Skill(name="sql")])
    job_description = JobDescription(
        skills=[
            Skill(name="Python"),
            Skill(name="SQL"),
            Skill(name="Docker"),
        ]
    )

    result = analyze_skill_match(resume, job_description)

    # 2/3 = 66.67%
    assert result.match_percentage == 66.67
    assert result.matched == ["Python", "SQL"]
    assert result.missing == ["Docker"]
    print("[OK] Test partial match passed")


def test_skill_match_full():
    """Test perfect skill match."""
    resume = Resume(skills=[Skill(name="python"), Skill(name="java")])
    job_description = JobDescription(
        skills=[
            Skill(name="Python"),
            Skill(name="Java"),
        ]
    )

    result = analyze_skill_match(resume, job_description)
    assert result.match_percentage == 100.0
    assert result.matched == ["Python", "Java"]
    assert result.missing == []
    print("[OK] Test full match passed")


if __name__ == "__main__":
    print("Running skill intelligence module tests...\n")
    test_skill_match_no_jd_skills()
    test_skill_match_partial()
    test_skill_match_full()
    print("\n[SUCCESS] All skill intelligence tests passed successfully!")

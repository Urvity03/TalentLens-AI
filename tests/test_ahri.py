"""Test the AHRI calculation module."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modules.models import Resume, JobDescription, Skill, SimilarityResult
from modules.ahri import calculate_ahri
from modules.jd_parser import parse_job_description
from modules.parser import parse_resume
from modules.similarity import calculate_resume_similarity


def test_ahri_mock_perfect_match():
    """Test AHRI with a mock perfect match."""
    resume = Resume(skills=[Skill(name="Python"), Skill(name="FastAPI")])
    job_description = JobDescription(skills=[Skill(name="Python"), Skill(name="FastAPI")])
    similarity = SimilarityResult(summary=85.0, skills=85.0, experience=85.0, overall=85.0)

    result = calculate_ahri(resume, job_description, similarity)

    # 85.0 + 2 (bonus) - 0 (penalty) = 87.0
    assert result.score == 87.0
    assert result.grade == "A"
    assert result.strengths == ["Python", "FastAPI"]
    assert result.missing_skills == []
    assert result.recommendation == "Excellent match for this position."
    print("[OK] Mock perfect match passed")


def test_ahri_mock_partial_match():
    """Test AHRI with some missing skills and limit bounds."""
    # 12 skills matching, 22 missing
    resume_skills = [Skill(name=f"Skill{i}") for i in range(12)]
    jd_skills = [Skill(name=f"Skill{i}") for i in range(12 + 22)]

    resume = Resume(skills=resume_skills)
    job_description = JobDescription(skills=jd_skills)
    similarity = SimilarityResult(summary=50.0, skills=50.0, experience=50.0, overall=50.0)

    result = calculate_ahri(resume, job_description, similarity)

    # Base: 50.0
    # Bonus: +12 -> capped at +10
    # Penalty: -22 * 0.5 = -11.0 -> capped at -10.0
    # Score = 50.0 + 10.0 - 10.0 = 50.0
    assert result.score == 50.0
    assert result.grade == "D"
    assert len(result.strengths) == 12
    assert len(result.missing_skills) == 22
    assert result.recommendation.startswith("Learn the following skills to improve your hiring readiness:")
    print("[OK] Mock partial match with cap bounds passed")


def test_ahri_integration():
    """Test AHRI using real parsed resume and JD."""
    resume = parse_resume("samples/resumes/sample_resume.pdf")
    job = parse_job_description("samples/job_descriptions/sample_jd.txt")
    similarity = calculate_resume_similarity(resume, job)

    result = calculate_ahri(resume, job, similarity)

    print(f"\nIntegration Test Output:")
    print(f"Overall Similarity: {similarity.overall}")
    print(f"AHRI Score:         {result.score}")
    print(f"AHRI Grade:         {result.grade}")
    print(f"Strengths:          {result.strengths}")
    print(f"Missing Skills:     {result.missing_skills}")
    print(f"Recommendation:     {result.recommendation}")

    assert 0 <= result.score <= 100
    assert result.grade in ["A+", "A", "B", "C", "D", "F"]
    print("[OK] Integration test passed")


if __name__ == "__main__":
    print("Running AHRI module tests...\n")
    test_ahri_mock_perfect_match()
    test_ahri_mock_partial_match()
    test_ahri_integration()
    print("\n[SUCCESS] All AHRI tests passed successfully!")

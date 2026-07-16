"""Integration test for the central candidate analyzer service."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modules.models import AnalysisResult
from services.analyzer import analyze_candidate


def test_analyzer_integration():
    """Verify that analyze_candidate orchestrates the entire pipeline correctly."""
    resume_path = "samples/resumes/sample_resume.pdf"
    jd_path = "samples/job_descriptions/sample_jd.txt"

    result = analyze_candidate(resume_path, jd_path)

    assert isinstance(result, AnalysisResult)

    # Use attribute access to verify
    assert result.resume is not None
    assert result.job_description is not None
    assert result.similarity is not None
    assert isinstance(result.quality, float)
    assert result.skill_intelligence is not None
    assert result.ahri is not None
    assert result.potential is not None
    assert result.recruiter is not None
    assert result.roadmap is not None

    print("Integration test passed successfully!")
    print(f"Verified fields: resume, job_description, similarity, quality, "
          f"skill_intelligence, ahri, potential, recruiter, roadmap")


if __name__ == "__main__":
    print("Running candidate analyzer integration test...\n")
    test_analyzer_integration()
    print("\n[SUCCESS] Integration test passed!")

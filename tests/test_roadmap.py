"""Test the career roadmap module."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modules.models import SkillIntelligence
from modules.roadmap import generate_career_roadmap


def test_roadmap_no_missing_skills():
    """Test roadmap generation when no skills are missing."""
    si = SkillIntelligence(matched=["Python", "SQL"], missing=[], match_percentage=100.0)
    roadmap = generate_career_roadmap(si)
    assert len(roadmap.steps) == 1
    assert roadmap.steps[0] == "Continue building real-world projects and keep your skills up to date."
    print("[OK] Test no missing skills passed")


def test_roadmap_generic_skill():
    """Test roadmap generation for a generic skill not in custom map."""
    si = SkillIntelligence(matched=["Python"], missing=["Go"], match_percentage=50.0)
    roadmap = generate_career_roadmap(si)
    assert len(roadmap.steps) == 1
    assert roadmap.steps[0] == "Learn Go and complete at least one practical project."
    print("[OK] Test generic skill passed")


def test_roadmap_custom_skills():
    """Test roadmap generation for custom AI/ML/dev skills."""
    si = SkillIntelligence(
        matched=[],
        missing=["Python", "PyTorch", "Docker"],
        match_percentage=0.0
    )
    roadmap = generate_career_roadmap(si)
    assert len(roadmap.steps) == 3
    assert "Master Python fundamentals" in roadmap.steps[0]
    assert "Master PyTorch tensors" in roadmap.steps[1]
    assert "containerization concepts" in roadmap.steps[2]
    print("[OK] Test custom skills passed")


if __name__ == "__main__":
    print("Running roadmap module tests...\n")
    test_roadmap_no_missing_skills()
    test_roadmap_generic_skill()
    test_roadmap_custom_skills()
    print("\n[SUCCESS] All roadmap tests passed successfully!")

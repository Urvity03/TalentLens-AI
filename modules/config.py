"""Project configuration values for TalentLens-AI."""

import re


SECTION_NAMES = (
    "Summary",
    "Skills",
    "Experience",
    "Education",
    "Projects",
    "Certifications",
    "Internship",
    "Achievements",
)

SECTION_PATTERN = re.compile(
    r"(?im)^\s*(professional\s+summary|summary|technical\s+skills|skills|"
    r"internship\s+experience|internship|experience|education|projects|"
    r"certifications|achievements)\s*:?\s*$"
)

SUPPORTED_SKILLS = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Data Science",
    "NLP",
    "Computer Vision",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "Flask",
    "FastAPI",
    "Streamlit",
    "Docker",
    "AWS",
    "Git",
    "GitHub",
]

SIMILARITY_WEIGHTS = {
    "summary": 0.2,
    "skills": 0.5,
    "experience": 0.3,
}

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

AHRI_GRADES = [
    (90, "A+"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (0, "F"),
]

AHRI_SKILL_BONUS = 1.0
AHRI_MAX_BONUS = 10.0

AHRI_SKILL_PENALTY = 0.5
AHRI_MAX_PENALTY = 10.0
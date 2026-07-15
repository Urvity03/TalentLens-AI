"""Project configuration values for TalentLens-AI."""

import re


SECTION_NAMES = (
    "Summary",
    "Skills",
    "Experience",
    "Education",
    "Projects",
    "Certifications",
)

SECTION_PATTERN = re.compile(
    r"(?im)^\s*(summary|skills|experience|education|projects|certifications)\s*:?\s*$"
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
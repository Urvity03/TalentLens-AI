"""Semantic similarity between a resume and a job description."""

from numpy import ndarray
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from modules.config import EMBEDDING_MODEL, SIMILARITY_WEIGHTS
from modules.models import (
    JobDescription,
    Resume,
    SimilarityResult,
)

_MODEL = None


def _load_model() -> SentenceTransformer:
    """Load the embedding model once."""

    global _MODEL

    if _MODEL is None:
        _MODEL = SentenceTransformer(EMBEDDING_MODEL)

    return _MODEL


def _encode(text: str) -> ndarray:
    """Convert text into an embedding."""

    return _load_model().encode(
        text or "",
        convert_to_numpy=True,
    )


def _similarity(text1: str, text2: str) -> float:
    """Return semantic similarity between two texts."""

    score = cosine_similarity(
        [_encode(text1)],
        [_encode(text2)],
    )[0][0]

    return round(float(score) * 100, 2)


def calculate_resume_similarity(
    resume: Resume,
    job_description: JobDescription,
) -> SimilarityResult:
    """Calculate semantic similarity between a resume and a job description."""

    summary = _similarity(
        resume.summary,
        job_description.summary,
    )

    skills = _similarity(
        " ".join(skill.name for skill in resume.skills),
        " ".join(skill.name for skill in job_description.skills),
    )

    experience = _similarity(
        " ".join(exp.description for exp in resume.experience),
        job_description.experience,
    )

    overall = float(
        round(
            summary * SIMILARITY_WEIGHTS["summary"]
            + skills * SIMILARITY_WEIGHTS["skills"]
            + experience * SIMILARITY_WEIGHTS["experience"],
            2,
        )
    )

    return SimilarityResult(
        summary=summary,
        skills=skills,
        experience=experience,
        overall=overall,
    )
"""Candidate analysis orchestration service."""

from pathlib import Path

from modules.ahri import calculate_ahri
from modules.evidence_intelligence import compile_evidence_collection
from modules.jd_parser import parse_job_description
from modules.models import AnalysisResult
from modules.parser import parse_resume
from modules.potential_predictor import predict_candidate_potential
from modules.quality_score import calculate_resume_quality
from modules.recruiter_insights import generate_recruiter_insights
from modules.roadmap import generate_career_roadmap
from modules.similarity import calculate_resume_similarity
from modules.skill_intelligence import analyze_skill_match


def analyze_candidate(
    resume_path: str | Path,
    job_description_path: str | Path,
) -> AnalysisResult:
    """Orchestrate the entire candidate profile and job description analysis pipeline.

    Args:
        resume_path: Path to the resume document (PDF/DOCX).
        job_description_path: Path to the job description text file.

    Returns:
        An AnalysisResult containing all computed pipeline models and details.
    """
    resume = parse_resume(resume_path)
    job_description = parse_job_description(job_description_path)

    # Compile the internal evidence collection
    evidence_collection = compile_evidence_collection(resume)

    similarity = calculate_resume_similarity(resume, job_description)
    quality = calculate_resume_quality(resume)
    skill_intelligence = analyze_skill_match(resume, job_description)

    ahri = calculate_ahri(resume, job_description, similarity)
    potential = predict_candidate_potential(ahri, skill_intelligence, quality)

    recruiter = generate_recruiter_insights(ahri, skill_intelligence, quality, potential)
    roadmap = generate_career_roadmap(skill_intelligence)

    return AnalysisResult(
        resume=resume,
        job_description=job_description,
        similarity=similarity,
        quality=quality,
        skill_intelligence=skill_intelligence,
        ahri=ahri,
        potential=potential,
        recruiter=recruiter,
        roadmap=roadmap,
    )

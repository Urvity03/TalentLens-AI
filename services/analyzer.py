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
    progress_callback=None,
) -> AnalysisResult:
    """Orchestrate the entire candidate profile and job description analysis pipeline.

    Args:
        resume_path: Path to the resume document (PDF/DOCX).
        job_description_path: Path to the job description text file.
        progress_callback: Optional callable for reporting progress steps.

    Returns:
        An AnalysisResult containing all computed pipeline models and details.
    """
    if progress_callback:
        progress_callback("Parsing Resume...", 10)
    resume = parse_resume(resume_path)

    if progress_callback:
        progress_callback("Parsing Job Description...", 25)
    job_description = parse_job_description(job_description_path)

    if progress_callback:
        progress_callback("Extracting Candidate Information...", 40)
    # Compile the internal evidence collection
    evidence_collection = compile_evidence_collection(resume)

    if progress_callback:
        progress_callback("Matching Candidate Skills...", 55)
    similarity = calculate_resume_similarity(resume, job_description)

    if progress_callback:
        progress_callback("Calculating Resume Quality...", 65)
    quality = calculate_resume_quality(resume)

    if progress_callback:
        progress_callback("Running Skill Intelligence...", 75)
    skill_intelligence = analyze_skill_match(resume, job_description)

    if progress_callback:
        progress_callback("Computing AHRI Score...", 85)
    ahri = calculate_ahri(resume, job_description, similarity)

    if progress_callback:
        progress_callback("Predicting Candidate Potential...", 90)
    potential = predict_candidate_potential(ahri, skill_intelligence, quality)

    if progress_callback:
        progress_callback("Generating Recruiter Insights...", 95)
    recruiter = generate_recruiter_insights(ahri, skill_intelligence, quality, potential)

    if progress_callback:
        progress_callback("Preparing Dashboard...", 98)
    roadmap = generate_career_roadmap(skill_intelligence)

    if progress_callback:
        progress_callback("Complete", 100)

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

"""Evidence Intelligence layer for TalentLens-AI.

Responsible only for collecting, classifying, and referencing evidence
without evaluation or scoring.
"""

from dataclasses import dataclass, field
import re

from modules.models import (
    CandidateProfile,
    EvidenceCategory,
    EvidenceCollection,
    EvidenceItem,
    EvidenceSource,
    TechnicalEvidence,
    ExperienceEvidence,
    ProjectEvidence,
    EducationEvidence,
    CertificationEvidence,
    ResumeEvidence,
    Skill,
)

# Deterministic Action Verbs and Project Complexity Keywords
ACTION_VERBS = {
    "developed", "implemented", "led", "created", "built", "optimized",
    "designed", "architected", "collaborated", "managed", "conducted", "applying",
    "mentored", "served", "worked"
}

COMPLEXITY_KEYWORDS = {
    "distributed", "scalable", "high performance", "optimization", "gpu", "pipeline", "deployment"
}


def _build_technical_evidence(profile: CandidateProfile) -> TechnicalEvidence:
    """Classify candidate skills into an immutable TechnicalEvidence profile.

    Args:
        profile: Candidate profile (Resume) object.

    Returns:
        TechnicalEvidence object containing categorized skills.
    """
    classified = set()
    for s_list in [
        profile.technical_profile.programming_languages,
        profile.technical_profile.frameworks,
        profile.technical_profile.libraries,
        profile.technical_profile.databases,
        profile.technical_profile.cloud,
        profile.technical_profile.developer_tools,
        profile.technical_profile.ml_tools,
        profile.technical_profile.soft_skills
    ]:
        for s in s_list:
            classified.add(s.lower().strip())

    # Find uncategorized skills
    uncategorized_skills = []
    for s in profile.skills:
        if s.name.lower().strip() not in classified:
            uncategorized_skills.append(s.name)

    def make_items(skills_list: list[str], sub_cat: str) -> tuple[EvidenceItem, ...]:
        items = []
        for i, s in enumerate(skills_list):
            source = EvidenceSource(section="Skills", block_index=0, raw_text=s)
            items.append(
                EvidenceItem(
                    id=f"tech_{sub_cat}_{i}",
                    category=EvidenceCategory.TECHNICAL,
                    content=s,
                    tags=(sub_cat,),
                    source=source
                )
            )
        return tuple(items)

    return TechnicalEvidence(
        programming_languages=make_items(profile.technical_profile.programming_languages, "languages"),
        frameworks=make_items(profile.technical_profile.frameworks, "frameworks"),
        libraries=make_items(profile.technical_profile.libraries, "libraries"),
        databases=make_items(profile.technical_profile.databases, "databases"),
        cloud=make_items(profile.technical_profile.cloud, "cloud"),
        developer_tools=make_items(profile.technical_profile.developer_tools, "tools"),
        ml_tools=make_items(profile.technical_profile.ml_tools, "ml"),
        soft_skills=make_items(profile.technical_profile.soft_skills, "soft"),
        uncategorized=make_items(uncategorized_skills, "uncategorized"),
    )


def _build_experience_evidence(profile: CandidateProfile) -> ExperienceEvidence:
    """Group experience timeline entries into specific categories.

    Args:
        profile: Candidate profile (Resume) object.

    Returns:
        ExperienceEvidence object containing categorized experiences.
    """
    relevant = []
    leadership = []
    internships = []
    freelance = []

    for i, exp in enumerate(profile.experience):
        source = EvidenceSource(section="Experience", block_index=i, raw_text=exp.description)
        role_title = f"{exp.title or 'Professional Role'} at {exp.company or 'Company'}"

        item = EvidenceItem(
            id=f"exp_role_{i}",
            category=EvidenceCategory.EXPERIENCE,
            content=role_title,
            tags=("role",),
            source=source
        )
        relevant.append(item)

        desc_lower = exp.description.lower()
        title_lower = (exp.title or "").lower()

        # Leadership Check
        lead_keywords = {"lead", "manage", "mentor", "coordinate", "direct", "supervise", "head", "architect"}
        if any(kw in desc_lower or kw in title_lower for kw in lead_keywords):
            leadership.append(
                EvidenceItem(
                    id=f"exp_lead_{i}",
                    category=EvidenceCategory.EXPERIENCE,
                    content=f"Leadership indicator in: {role_title}",
                    tags=("leadership",),
                    source=source
                )
            )

        # Internship Check
        if "intern" in title_lower or "intern" in desc_lower:
            internships.append(
                EvidenceItem(
                    id=f"exp_intern_{i}",
                    category=EvidenceCategory.EXPERIENCE,
                    content=f"Internship: {role_title}",
                    tags=("internship",),
                    source=source
                )
            )

        # Contract Check
        contract_keywords = {"freelance", "contract", "consultant"}
        if any(kw in title_lower or kw in desc_lower for kw in contract_keywords):
            freelance.append(
                EvidenceItem(
                    id=f"exp_contract_{i}",
                    category=EvidenceCategory.EXPERIENCE,
                    content=f"Contract/Freelance: {role_title}",
                    tags=("contract",),
                    source=source
                )
            )

    return ExperienceEvidence(
        relevant_roles=tuple(relevant),
        leadership_indicators=tuple(leadership),
        internships=tuple(internships),
        freelance_or_contract=tuple(freelance),
    )


def _build_project_evidence(profile: CandidateProfile) -> ProjectEvidence:
    """Group project timeline entries into specific categories.

    Args:
        profile: Candidate profile (Resume) object.

    Returns:
        ProjectEvidence object containing categorized projects.
    """
    deployed = []
    academic = []
    complexity = []

    for i, proj in enumerate(profile.projects):
        source = EvidenceSource(section="Projects", block_index=i, raw_text=proj.description)
        desc_lower = proj.description.lower()
        title = proj.title or "Project"

        # Production Check
        if proj.demo or any(kw in desc_lower for kw in ["deploy", "host", "live", "production"]):
            deployed.append(
                EvidenceItem(
                    id=f"proj_dep_{i}",
                    category=EvidenceCategory.PROJECT,
                    content=f"Deployed project: {title}",
                    tags=("production", "deployed"),
                    source=source
                )
            )

        # Academic Check
        if not proj.demo and any(kw in desc_lower for kw in ["academic", "research", "thesis", "course", "classroom", "university"]):
            academic.append(
                EvidenceItem(
                    id=f"proj_acad_{i}",
                    category=EvidenceCategory.PROJECT,
                    content=f"Academic/Research project: {title}",
                    tags=("academic", "research"),
                    source=source
                )
            )

        # Complexity Check
        matched_complexity = [kw for kw in COMPLEXITY_KEYWORDS if kw in desc_lower]
        if matched_complexity:
            complexity.append(
                EvidenceItem(
                    id=f"proj_comp_{i}",
                    category=EvidenceCategory.PROJECT,
                    content=f"Project complexity in {title}: mentions {', '.join(matched_complexity)}",
                    tags=tuple(matched_complexity),
                    source=source
                )
            )

    return ProjectEvidence(
        production_or_deployed=tuple(deployed),
        academic_or_research=tuple(academic),
        complexity_indicators=tuple(complexity),
    )


def _build_education_evidence(profile: CandidateProfile) -> EducationEvidence:
    """Collect education records without quality evaluation.

    Args:
        profile: Candidate profile (Resume) object.

    Returns:
        EducationEvidence object containing structured academics.
    """
    degrees = []
    coursework = []
    performance = []

    for i, edu in enumerate(profile.education):
        source = EvidenceSource(section="Education", block_index=i, raw_text=edu.description)
        deg_str = f"{edu.degree or 'Degree'} in {edu.major or 'Major'} at {edu.institution or 'Institution'}"

        degrees.append(
            EvidenceItem(
                id=f"edu_deg_{i}",
                category=EvidenceCategory.EDUCATION,
                content=deg_str,
                tags=("degree",),
                source=source
            )
        )

        desc_lower = edu.description.lower()
        if "course" in desc_lower or "subject" in desc_lower or "module" in desc_lower:
            coursework.append(
                EvidenceItem(
                    id=f"edu_course_{i}",
                    category=EvidenceCategory.EDUCATION,
                    content=f"Coursework listed in: {edu.institution}",
                    tags=("coursework",),
                    source=source
                )
            )

        if edu.gpa:
            performance.append(
                EvidenceItem(
                    id=f"edu_perf_{i}",
                    category=EvidenceCategory.EDUCATION,
                    content=f"Academic score: {edu.gpa} at {edu.institution}",
                    tags=("gpa", "performance"),
                    source=source
                )
            )

    return EducationEvidence(
        degrees=tuple(degrees),
        coursework=tuple(coursework),
        performance_markers=tuple(performance),
    )


def _build_certification_evidence(profile: CandidateProfile) -> CertificationEvidence:
    """Group certification listings.

    Args:
        profile: Candidate profile (Resume) object.

    Returns:
        CertificationEvidence object containing categorized certifications.
    """
    vendor = []
    industry = []

    vendor_keywords = {"ibm", "google", "aws", "microsoft", "oracle"}

    for i, cert in enumerate(profile.certifications):
        source = EvidenceSource(section="Certifications", block_index=i, raw_text=cert.description)
        org_lower = (cert.organization or "").lower()

        cert_item = EvidenceItem(
            id=f"cert_{i}",
            category=EvidenceCategory.CERTIFICATION,
            content=f"{cert.name} (Issued by: {cert.organization or 'Not Specified'})",
            tags=("certification",),
            source=source
        )

        if any(v in org_lower for v in vendor_keywords) or any(v in cert.name.lower() for v in vendor_keywords):
            vendor.append(cert_item)
        else:
            industry.append(cert_item)

    return CertificationEvidence(
        vendor_certifications=tuple(vendor),
        industry_certifications=tuple(industry),
    )


def _build_resume_evidence(profile: CandidateProfile) -> ResumeEvidence:
    """Extract metrics, action verbs, and achievements.

    Args:
        profile: Candidate profile (Resume) object.

    Returns:
        ResumeEvidence object containing extracted timeline artifacts.
    """
    metrics = []
    action_verbs = []
    awards = []

    item_counter = 0
    for i, exp in enumerate(profile.experience):
        source = EvidenceSource(section="Experience", block_index=i, raw_text=exp.description)

        if any(kw in exp.description.lower() for kw in ["award", "honor", "win", "rank", "competit", "hackathon"]):
            item_counter += 1
            awards.append(
                EvidenceItem(
                    id=f"res_award_{item_counter}",
                    category=EvidenceCategory.RESUME,
                    content=f"Achievement index: {exp.title or 'Role'}",
                    tags=("award", "achievement"),
                    source=source
                )
            )

        for line in exp.description.splitlines():
            line_strip = line.strip().lower()
            if not line_strip:
                continue

            if "%" in line_strip or any(char.isdigit() for char in line_strip):
                # Filter out raw phone details or calendar years
                if "@" not in line_strip and not re.search(r"\b\d{4}\b", line_strip):
                    item_counter += 1
                    metrics.append(
                        EvidenceItem(
                            id=f"res_metric_{item_counter}",
                            category=EvidenceCategory.RESUME,
                            content=line.strip(),
                            tags=("metric",),
                            source=source
                        )
                    )

            words = re.sub(r"^[^a-zA-Z]+", "", line_strip).split()
            first_word = words[0] if words else ""
            if first_word in ACTION_VERBS:
                item_counter += 1
                action_verbs.append(
                    EvidenceItem(
                        id=f"res_verb_{item_counter}",
                        category=EvidenceCategory.RESUME,
                        content=line.strip(),
                        tags=("action_verb", first_word),
                        source=source
                    )
                )

    return ResumeEvidence(
        metrics=tuple(metrics),
        action_verbs=tuple(action_verbs),
        awards_and_achievements=tuple(awards),
    )


def compile_evidence_collection(profile: CandidateProfile) -> EvidenceCollection:
    """Orchestrate compilation of the immutable EvidenceCollection.

    Args:
        profile: Structured CandidateProfile (Resume).

    Returns:
        An immutable, type-safe, traceable EvidenceCollection object.
    """
    return EvidenceCollection(
        technical=_build_technical_evidence(profile),
        experience=_build_experience_evidence(profile),
        project=_build_project_evidence(profile),
        education=_build_education_evidence(profile),
        certification=_build_certification_evidence(profile),
        resume=_build_resume_evidence(profile),
    )

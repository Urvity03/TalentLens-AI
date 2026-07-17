"""Shared data models for TalentLens-AI."""

from dataclasses import dataclass, field
from enum import Enum


# ---------- Contact ----------

@dataclass
class ContactInfo:
    """Candidate contact information."""

    name: str | None = None
    email: str | None = None
    phone: str | None = None
    linkedin: str | None = None
    github: str | None = None
    portfolio: str | None = None
    location: str | None = None


# ---------- Common ----------

@dataclass
class Skill:
    """Detected skill."""

    name: str
    confidence: float = 1.0


# ---------- Professional Identity ----------

@dataclass
class ProfessionalIdentity:
    """Professional identity of the candidate."""

    current_title: str | None = None
    career_focus: str | None = None
    primary_domain: str | None = None
    technical_specialization: str | None = None


# ---------- Technical Profile ----------

@dataclass
class TechnicalProfile:
    """Classified technical profile categories of the candidate."""

    programming_languages: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)
    libraries: list[str] = field(default_factory=list)
    databases: list[str] = field(default_factory=list)
    cloud: list[str] = field(default_factory=list)
    developer_tools: list[str] = field(default_factory=list)
    ml_tools: list[str] = field(default_factory=list)
    soft_skills: list[str] = field(default_factory=list)


# ---------- Resume Sections ----------

@dataclass
class Experience:
    """Experience section."""

    description: str
    title: str | None = None
    company: str | None = None
    duration: str | None = None
    technologies: list[str] = field(default_factory=list)
    achievements: list[str] = field(default_factory=list)


@dataclass
class Education:
    """Education section."""

    description: str
    degree: str | None = None
    institution: str | None = None
    dates: str | None = None
    major: str | None = None
    gpa: str | None = None


@dataclass
class Project:
    """Project section."""

    description: str
    title: str | None = None
    technologies: list[str] = field(default_factory=list)
    domain: str | None = None
    github: str | None = None
    demo: str | None = None
    key_achievements: list[str] = field(default_factory=list)


@dataclass
class Certification:
    """Certification section."""

    description: str
    name: str | None = None
    organization: str | None = None
    date: str | None = None
    credential_url: str | None = None


# ---------- Main Objects ----------

@dataclass
class Resume:
    """Structured resume representing the complete Candidate Profile."""

    contact: ContactInfo = field(default_factory=ContactInfo)
    summary: str = ""

    skills: list[Skill] = field(default_factory=list)
    experience: list[Experience] = field(default_factory=list)
    education: list[Education] = field(default_factory=list)
    projects: list[Project] = field(default_factory=list)
    certifications: list[Certification] = field(default_factory=list)

    professional_identity: ProfessionalIdentity = field(default_factory=ProfessionalIdentity)
    technical_profile: TechnicalProfile = field(default_factory=TechnicalProfile)


# Type Alias to support the CandidateProfile name from specifications
CandidateProfile = Resume


@dataclass
class JobDescription:
    """Structured job description."""

    title: str = ""
    summary: str = ""

    skills: list[Skill] = field(default_factory=list)

    experience: str = ""
    education: str = ""


@dataclass
class SimilarityResult:
    """Semantic similarity scores."""

    summary: float = 0.0
    skills: float = 0.0
    experience: float = 0.0
    overall: float = 0.0


@dataclass
class AHRIResult:
    """Adaptive Hiring Readiness Index."""

    score: float
    grade: str
    strengths: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    recommendation: str = ""


@dataclass
class SkillIntelligence:
    """Skill intelligence match results."""

    matched: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    match_percentage: float = 0.0


@dataclass
class PotentialPrediction:
    """Candidate potential prediction."""

    score: float
    level: str


@dataclass
class CareerRoadmap:
    """Personalized learning roadmap."""

    steps: list[str] = field(default_factory=list)


@dataclass
class RecruiterInsights:
    """Recruiter summary."""

    strengths: list[str] = field(default_factory=list)
    concerns: list[str] = field(default_factory=list)
    recommendation: str = ""


@dataclass
class AnalysisResult:
    """Consolidated candidate analysis pipeline results."""

    resume: Resume
    job_description: JobDescription
    similarity: SimilarityResult
    quality: float
    skill_intelligence: SkillIntelligence
    ahri: AHRIResult
    potential: PotentialPrediction
    recruiter: RecruiterInsights
    roadmap: CareerRoadmap


# ---------- Evidence Intelligence (Milestone 2) ----------

class EvidenceCategory(Enum):
    """Categories of candidate evidence."""

    TECHNICAL = "technical"
    EXPERIENCE = "experience"
    PROJECT = "project"
    EDUCATION = "education"
    CERTIFICATION = "certification"
    RESUME = "resume"


@dataclass(frozen=True)
class EvidenceSource:
    """The origin tracer for an evidence item."""

    section: str
    block_index: int
    raw_text: str
    page_number: int | None = None
    line_number: int | None = None
    confidence: float = 1.0


@dataclass(frozen=True)
class EvidenceItem:
    """A single piece of structured evidence."""

    id: str
    category: EvidenceCategory
    content: str
    tags: tuple[str, ...]
    source: EvidenceSource


@dataclass(frozen=True)
class TechnicalEvidence:
    """Categorized technical skills evidence list."""

    programming_languages: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    frameworks: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    libraries: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    databases: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    cloud: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    developer_tools: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    ml_tools: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    soft_skills: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    uncategorized: tuple[EvidenceItem, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ExperienceEvidence:
    """Grouped career and employment history evidence list."""

    relevant_roles: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    leadership_indicators: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    internships: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    freelance_or_contract: tuple[EvidenceItem, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ProjectEvidence:
    """Grouped project achievements, complex architectures and domains."""

    production_or_deployed: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    academic_or_research: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    complexity_indicators: tuple[EvidenceItem, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class EducationEvidence:
    """Academic achievements, degrees, major courses and performance markers."""

    degrees: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    coursework: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    performance_markers: tuple[EvidenceItem, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class CertificationEvidence:
    """Vendor, university, and industry credentials."""

    vendor_certifications: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    industry_certifications: tuple[EvidenceItem, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ResumeEvidence:
    """Extracted numeric achievements, action verbs and awards."""

    metrics: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    action_verbs: tuple[EvidenceItem, ...] = field(default_factory=tuple)
    awards_and_achievements: tuple[EvidenceItem, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class EvidenceCollection:
    """Unified internal read-only collection of candidate evidence."""

    technical: TechnicalEvidence = field(default_factory=TechnicalEvidence)
    experience: ExperienceEvidence = field(default_factory=ExperienceEvidence)
    project: ProjectEvidence = field(default_factory=ProjectEvidence)
    education: EducationEvidence = field(default_factory=EducationEvidence)
    certification: CertificationEvidence = field(default_factory=CertificationEvidence)
    resume: ResumeEvidence = field(default_factory=ResumeEvidence)
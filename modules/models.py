"""Shared data models for TalentLens-AI."""

from dataclasses import dataclass, field


# ---------- Contact ----------

@dataclass
class ContactInfo:
    """Candidate contact information."""

    name: str | None = None
    email: str | None = None
    phone: str | None = None
    linkedin: str | None = None
    github: str | None = None


# ---------- Common ----------

@dataclass
class Skill:
    """Detected skill."""

    name: str
    confidence: float = 1.0


# ---------- Resume Sections ----------

@dataclass
class Experience:
    """Experience section."""

    description: str
    title: str | None = None
    company: str | None = None


@dataclass
class Education:
    """Education section."""

    description: str
    degree: str | None = None
    institution: str | None = None


@dataclass
class Project:
    """Project section."""

    description: str
    title: str | None = None


@dataclass
class Certification:
    """Certification section."""

    description: str
    name: str | None = None


# ---------- Main Objects ----------

@dataclass
class Resume:
    """Structured resume."""

    contact: ContactInfo = field(default_factory=ContactInfo)
    summary: str = ""

    skills: list[Skill] = field(default_factory=list)
    experience: list[Experience] = field(default_factory=list)
    education: list[Education] = field(default_factory=list)
    projects: list[Project] = field(default_factory=list)
    certifications: list[Certification] = field(default_factory=list)


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
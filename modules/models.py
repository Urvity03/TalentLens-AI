"""Shared data models for TalentLens-AI."""

from dataclasses import dataclass, field


@dataclass
class ContactInfo:
    """Candidate contact information."""

    name: str | None = None
    email: str | None = None
    phone: str | None = None
    linkedin: str | None = None
    github: str | None = None


@dataclass
class Skill:
    """Detected skill from a resume or job description."""

    name: str
    confidence: float = 1.0


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


@dataclass
class Resume:
    """Structured resume object."""

    contact: ContactInfo = field(default_factory=ContactInfo)
    summary: str = ""

    skills: list[Skill] = field(default_factory=list)
    experience: list[Experience] = field(default_factory=list)
    education: list[Education] = field(default_factory=list)
    projects: list[Project] = field(default_factory=list)
    certifications: list[Certification] = field(default_factory=list)
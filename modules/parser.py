"""Parse preprocessed resume data into a Resume object."""

from pathlib import Path
import re

from modules.models import (
    Certification,
    ContactInfo,
    Education,
    Experience,
    Project,
    Resume,
    Skill,
    ProfessionalIdentity,
    TechnicalProfile,
)
from modules.preprocess import preprocess_file
from modules.skill_extractor import extract_skills

EMAIL_PATTERN = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
PHONE_PATTERN = re.compile(r"\+?\d[\d\s\-()]{8,}\d")


def _extract_contact(text: str) -> ContactInfo:
    """Extract candidate contact information.

    Args:
        text: Raw resume text content.

    Returns:
        A ContactInfo object populated with contact details.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    email_match = EMAIL_PATTERN.search(text)
    phone_match = PHONE_PATTERN.search(text)

    email = email_match.group() if email_match else None
    phone = phone_match.group() if phone_match else None

    linkedin = next((l for l in lines if "linkedin.com/in" in l.lower() or "linkedin.com" in l.lower()), None)
    if linkedin:
        linkedin_match = re.search(r"(linkedin\.com/in/[\w\-]+/?|linkedin\.com/[\w\-]+/?)", linkedin, re.IGNORECASE)
        if linkedin_match:
            linkedin = linkedin_match.group(1).strip()

    github = next((l for l in lines if "github.com" in l.lower()), None)
    if github:
        github_match = re.search(r"(github\.com/[\w\-]+/?)", github, re.IGNORECASE)
        if github_match:
            github = github_match.group(1).strip()

    # Find unique web links for portfolio URLs
    portfolio = None
    urls = re.findall(r"https?://[\w\.\-/]+", text)
    for url in urls:
        url_lower = url.lower()
        if "linkedin.com" not in url_lower and "github.com" not in url_lower:
            portfolio = url
            break

    # Location parsing logic
    location = None
    for line in lines[:8]:
        line_lower = line.lower()
        if "map-marker" in line_lower or "location:" in line_lower or "address:" in line_lower:
            location = re.sub(r"(?i)^map-marker(?:-alt)?\s*|location:\s*|address:\s*", "", line).strip()
            break
    if not location:
        # Check first 5 lines for standard comma-separated city formats
        for line in lines[1:5]:
            if "," in line and len(line) < 50:
                if "@" not in line and not any(k in line.lower() for k in ["linkedin.com", "github.com", "http"]):
                    if not any(char.isdigit() for char in line if char not in "+-() "):
                        location = line
                        break

    return ContactInfo(
        name=lines[0] if lines else None,
        email=email,
        phone=phone,
        linkedin=linkedin,
        github=github,
        portfolio=portfolio,
        location=location,
    )


def _extract_professional_identity(skills: list[Skill], experience: list[Experience]) -> ProfessionalIdentity:
    """Extract and map professional identity alignment rules based on skills and history.

    Args:
        skills: List of extracted technical skill objects.
        experience: List of experience items.

    Returns:
        A ProfessionalIdentity object mapping candidate focus areas.
    """
    current_title = None
    if experience:
        current_title = experience[0].title

    skill_names = {s.name.lower() for s in skills}

    focus = "Software Engineering"
    domain = "Technology"
    spec = "Full-Stack Development"

    if any(s in skill_names for s in ["machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch"]):
        focus = "Artificial Intelligence & Machine Learning"
        domain = "AI Hiring Intelligence"
        spec = "AI/ML Engineering"
    elif any(s in skill_names for s in ["python", "java", "c++", "c#", "backend", "go", "sql"]):
        focus = "Backend Engineering"
        domain = "Software Engineering"
        spec = "Backend Systems"
    elif any(s in skill_names for s in ["javascript", "typescript", "react", "html", "css", "angular", "vue"]):
        focus = "Frontend Engineering"
        domain = "Web Development"
        spec = "Frontend Systems"

    return ProfessionalIdentity(
        current_title=current_title,
        career_focus=focus,
        primary_domain=domain,
        technical_specialization=spec,
    )


def _classify_technical_profile(skills: list[Skill]) -> TechnicalProfile:
    """Classify candidate skills into distinct folder directories.

    Args:
        skills: Flat list of parsed Skill objects.

    Returns:
        A TechnicalProfile object mapping lists.
    """
    profile = TechnicalProfile()

    langs_set = {"python", "javascript", "java", "c++", "c#", "ruby", "go", "rust", "sql", "html", "css", "typescript", "swift", "kotlin"}
    frameworks_set = {"django", "flask", "fastapi", "streamlit", "react", "angular", "vue", "next.js", "bootstrap"}
    libs_set = {"pandas", "numpy", "scipy", "scikit-learn", "matplotlib", "seaborn", "nltk", "spacy"}
    db_set = {"sqlite", "postgresql", "mysql", "mongodb", "redis", "oracle", "mariadb", "cassandra"}
    cloud_set = {"aws", "gcp", "azure", "google cloud", "vertex ai", "heroku", "netlify"}
    tools_set = {"git", "github", "gitlab", "docker", "kubernetes", "k8s", "terraform", "ansible", "jenkins", "jira", "figma", "slack", "vscode", "linux"}
    ml_set = {"tensorflow", "pytorch", "keras", "opencv", "scikit-learn", "machine learning", "deep learning", "nlp", "natural language processing", "computer vision", "generative ai", "explainable ai", "xai"}
    soft_set = {"communication", "leadership", "teamwork", "problem solving", "agile", "scrum", "collaboration", "management", "mentoring", "critical thinking"}

    for s in skills:
        s_lower = s.name.lower().strip()
        if s_lower in langs_set:
            profile.programming_languages.append(s.name)
        elif s_lower in frameworks_set:
            profile.frameworks.append(s.name)
        elif s_lower in libs_set:
            profile.libraries.append(s.name)
        elif s_lower in db_set:
            profile.databases.append(s.name)
        elif s_lower in cloud_set:
            profile.cloud.append(s.name)
        elif s_lower in tools_set:
            profile.developer_tools.append(s.name)
        elif s_lower in ml_set:
            profile.ml_tools.append(s.name)
        elif s_lower in soft_set:
            profile.soft_skills.append(s.name)

    return profile


def _parse_education_blocks(text: str) -> list[Education]:
    """Parse education text block into structured Education records.

    Args:
        text: Education text block content.

    Returns:
        List of Education objects.
    """
    records = []
    text = text.strip()
    if not text:
        return records

    blocks = re.split(r"\n\s*\n", text)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        inst = lines[0].strip()

        dates = None
        degree_line = None

        if len(lines) > 1:
            second_line = lines[1].strip()
            # Detect dates via year patterns or expected keywords
            if re.search(r"\b(?:19|20)\d{2}\b|\b(?:Expected|Ongoing|Present)\b", second_line, re.IGNORECASE):
                dates = second_line
                if len(lines) > 2:
                    degree_line = lines[2].strip()
            else:
                degree_line = second_line

        degree = degree_line or "Not Specified"
        major = None
        if degree_line:
            parts = re.split(r"[–-]", degree_line)
            if len(parts) > 1:
                degree = parts[0].strip()
                major = parts[1].strip()

        # GPA validation parsing
        gpa = None
        gpa_match = re.search(r"\b(?:CGPA|GPA|Percentage)\s*[:\-]?\s*([0-9\.\%]+(?:\s*/\s*[0-9\.]+)?)\b", block, re.IGNORECASE)
        if gpa_match:
            gpa = gpa_match.group(1).strip()

        records.append(
            Education(
                description=block,
                degree=degree,
                institution=inst,
                dates=dates,
                major=major,
                gpa=gpa,
            )
        )
    return records


def _parse_experience_blocks(exp_text: str, intern_text: str) -> list[Experience]:
    """Parse experience and internships text blocks into structured Experience records.

    Args:
        exp_text: Experience text block content.
        intern_text: Internship text block content.

    Returns:
        List of Experience objects.
    """
    records = []

    def parse_blocks(block_text: str):
        blocks = re.split(r"\n\s*\n", block_text.strip())
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            lines = block.splitlines()
            first_line = lines[0].strip()

            duration = None
            desc_start_idx = 1
            if len(lines) > 1:
                second_line = lines[1].strip()
                if re.search(r"\b(?:19|20)\d{2}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Ongoing|Present)\b", second_line, re.IGNORECASE):
                    duration = second_line
                    desc_start_idx = 2

            description = "\n".join(lines[desc_start_idx:])

            # Parse achievements from bullet points
            achievements = []
            for line in lines[desc_start_idx:]:
                line_strip = line.strip()
                if line_strip.startswith("•") or line_strip.startswith("-") or line_strip.startswith("*"):
                    achievements.append(re.sub(r"^[•\-*]\s*", "", line_strip))

            company = None
            title = first_line
            if "IBM" in first_line:
                company = "IBM"
                title = re.sub(r"\bIBM\b\s*(?:Project-Based Learning \(PBL\) Internship \(Ongoing\)|Project-Based Learning \(PBL\) Internship|Internship)?", "", first_line).strip()
                title = re.sub(r"\s+", " ", title).strip()
            elif "Tata" in first_line:
                company = "Tata"
                title = re.sub(r"\bTata\b\s*(?:iQ\s*Virtual\s*Internship\s*–|iQ\s*Virtual\s*Internship|iQ)?", "", first_line).strip()
                title = re.sub(r"\s+", " ", title).strip()
            else:
                parts = re.split(r"[–-]", first_line)
                if len(parts) > 1:
                    company = parts[0].strip()
                    title = parts[1].strip()

            # Parse technologies used from within this experience block text
            from modules.config import SUPPORTED_SKILLS
            technologies = []
            block_lower = block.lower()
            for skill in SUPPORTED_SKILLS:
                if re.search(rf"\b{re.escape(skill.lower())}\b", block_lower):
                    technologies.append(skill)

            records.append(
                Experience(
                    description=description,
                    title=title,
                    company=company,
                    duration=duration,
                    technologies=technologies,
                    achievements=achievements,
                )
            )

    if exp_text.strip():
        parse_blocks(exp_text)
    if intern_text.strip():
        parse_blocks(intern_text)

    return records


def _parse_project_blocks(text: str) -> list[Project]:
    """Parse projects text block into structured Project records.

    Args:
        text: Projects text block content.

    Returns:
        List of Project objects.
    """
    records = []
    text = text.strip()
    if not text:
        return records

    blocks = re.split(r"\n\s*\n", text)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        title = lines[0].strip()

        github = None
        demo = None
        urls = re.findall(r"https?://[\w\.\-/]+", block)
        for url in urls:
            if "github.com" in url.lower():
                github = url
            else:
                demo = url

        key_achievements = []
        for line in lines[1:]:
            line_strip = line.strip()
            if line_strip.startswith("•") or line_strip.startswith("-") or line_strip.startswith("*"):
                key_achievements.append(re.sub(r"^[•\-*]\s*", "", line_strip))

        from modules.config import SUPPORTED_SKILLS
        technologies = []
        block_lower = block.lower()
        for skill in SUPPORTED_SKILLS:
            if re.search(rf"\b{re.escape(skill.lower())}\b", block_lower):
                technologies.append(skill)

        domain = "Software Development"
        tech_set = {t.lower() for t in technologies}
        if any(t in tech_set for t in ["tensorflow", "pytorch", "machine learning", "deep learning", "nlp"]):
            domain = "Artificial Intelligence"

        records.append(
            Project(
                description=block,
                title=title,
                technologies=technologies,
                domain=domain,
                github=github,
                demo=demo,
                key_achievements=key_achievements,
            )
        )
    return records


def _parse_certification_blocks(text: str) -> list[Certification]:
    """Parse certifications block into structured Certification records.

    Args:
        text: Certifications text block content.

    Returns:
        List of Certification objects.
    """
    records = []
    text = text.strip()
    if not text:
        return records

    parts = []
    for line in text.splitlines():
        for item in re.split(r"[•\n]", line):
            if item.strip():
                parts.append(item.strip())

    for part in parts:
        org = "Not Specified"
        if "IBM" in part:
            org = "IBM"
        elif "Google" in part:
            org = "Google"
        elif "AWS" in part:
            org = "AWS"

        records.append(
            Certification(
                description=part,
                name=part,
                organization=org,
                date=None,
                credential_url=None,
            )
        )
    return records


def parse_resume(file_path: str | Path) -> Resume:
    """Parse a resume file path into a Resume data model.

    Args:
        file_path: Absolute path to the resume file.

    Returns:
        A Resume object mapping all parsed candidate intelligence elements.
    """
    data = preprocess_file(file_path)
    sections = data["sections"]
    text = data["text"]

    contact = _extract_contact(text)
    skills = extract_skills(sections.get("Skills", ""))
    education = _parse_education_blocks(sections.get("Education", ""))
    experience = _parse_experience_blocks(
        sections.get("Experience", ""),
        sections.get("Internship", ""),
    )
    projects = _parse_project_blocks(sections.get("Projects", ""))
    certifications = _parse_certification_blocks(sections.get("Certifications", ""))

    professional_identity = _extract_professional_identity(skills, experience)
    technical_profile = _classify_technical_profile(skills)

    # Narrative auto-generation fallback
    summary = sections.get("Summary", "").strip()
    if not summary:
        name_str = contact.name or "The candidate"
        skills_str = ", ".join([s.name for s in skills[:4]])
        narrative_parts = [f"{name_str} is a professional candidate specializing in {skills_str}."]

        if experience:
            latest = experience[0]
            role = latest.title or "Professional Role"
            comp = latest.company or "Company"
            narrative_parts.append(f"Most recently worked as {role} at {comp}.")

        if education:
            latest_edu = education[0]
            deg = latest_edu.degree or "Degree"
            inst = latest_edu.institution or "Institution"
            narrative_parts.append(f"Academic background includes {deg} from {inst}.")

        summary = " ".join(narrative_parts)

    return Resume(
        contact=contact,
        summary=summary,
        skills=skills,
        experience=experience,
        education=education,
        projects=projects,
        certifications=certifications,
        professional_identity=professional_identity,
        technical_profile=technical_profile,
    )
"""Unit tests for the Candidate Intelligence parser and models."""

import unittest
from unittest.mock import patch
from pathlib import Path

from modules.models import Skill
from modules.parser import (
    parse_resume,
    _extract_contact,
    _extract_professional_identity,
    _classify_technical_profile,
    _parse_education_blocks,
    _parse_experience_blocks,
    _parse_project_blocks,
    _parse_certification_blocks,
)


class TestCandidateIntelligence(unittest.TestCase):
    """Test suite validating Candidate Intelligence parsing capability, heuristics, and models."""

    def test_contact_intelligence_extraction(self):
        """Verify contact intelligence name, email, phone, location, and web links extraction."""
        text = """Urvi Tyagi
        Phone: +91 8923643053
        Email: tyagiurvi03@gmail.com
        Address: Ghaziabad, Uttar Pradesh, India
        LinkedIn: linkedin.com/in/urvi-tyagi026
        GitHub: github.com/urvity03
        Portfolio: https://urvityagi.dev/portfolio
        """
        contact = _extract_contact(text)
        self.assertEqual(contact.name, "Urvi Tyagi")
        self.assertEqual(contact.email, "tyagiurvi03@gmail.com")
        self.assertEqual(contact.phone, "+91 8923643053")
        self.assertEqual(contact.linkedin, "linkedin.com/in/urvi-tyagi026")
        self.assertEqual(contact.github, "github.com/urvity03")
        self.assertEqual(contact.portfolio, "https://urvityagi.dev/portfolio")
        self.assertEqual(contact.location, "Ghaziabad, Uttar Pradesh, India")

    def test_contact_intelligence_missing_and_malformed(self):
        """Verify contact extraction gracefully handles missing, empty, and malformed inputs."""
        text = "Random Candidate Profile\nNo contact info present here."
        contact = _extract_contact(text)
        self.assertEqual(contact.name, "Random Candidate Profile")
        self.assertIsNone(contact.email)
        self.assertIsNone(contact.phone)
        self.assertIsNone(contact.linkedin)
        self.assertIsNone(contact.github)
        self.assertIsNone(contact.portfolio)
        self.assertIsNone(contact.location)

    def test_professional_identity_classification(self):
        """Verify professional identity maps specialized focus areas and domains from skills."""
        skills = [Skill("Python"), Skill("TensorFlow"), Skill("NLP")]
        experience = [_parse_experience_blocks("Senior ML Engineer\nIBM\nWorking on ML systems.", "")[0]]

        identity = _extract_professional_identity(skills, experience)
        self.assertEqual(identity.current_title, "Senior ML Engineer")
        self.assertEqual(identity.career_focus, "Artificial Intelligence & Machine Learning")
        self.assertEqual(identity.primary_domain, "AI Hiring Intelligence")
        self.assertEqual(identity.technical_specialization, "AI/ML Engineering")

    def test_technical_profile_categorization(self):
        """Verify technical profile classifies skills into distinct categories."""
        skills = [
            Skill("Python"),
            Skill("FastAPI"),
            Skill("Pandas"),
            Skill("PostgreSQL"),
            Skill("AWS"),
            Skill("Docker"),
            Skill("TensorFlow"),
            Skill("Teamwork"),
            Skill("UnknownSkillExample"),
        ]
        profile = _classify_technical_profile(skills)
        self.assertIn("Python", profile.programming_languages)
        self.assertIn("FastAPI", profile.frameworks)
        self.assertIn("Pandas", profile.libraries)
        self.assertIn("PostgreSQL", profile.databases)
        self.assertIn("AWS", profile.cloud)
        self.assertIn("Docker", profile.developer_tools)
        self.assertIn("TensorFlow", profile.ml_tools)
        self.assertIn("Teamwork", profile.soft_skills)

        # Confirm unrecognized skills are not discarded (they remain uncategorized in skills root list,
        # but don't cause failures in classification).
        self.assertNotIn("UnknownSkillExample", profile.programming_languages)

    def test_education_timeline_parsing(self):
        """Verify education timeline splits degrees, institutions, majors, and GPAs/Percentages."""
        text = """AKTU University
        Expected 2027
        Bachelor of Technology (B.Tech) – Computer Science
        GPA: 9.2/10
        
        Stanford University
        2021 - 2023
        Master of Science – Artificial Intelligence
        CGPA: 3.8/4.0
        """
        edu_list = _parse_education_blocks(text)
        self.assertEqual(len(edu_list), 2)

        self.assertEqual(edu_list[0].institution, "AKTU University")
        self.assertEqual(edu_list[0].dates, "Expected 2027")
        self.assertEqual(edu_list[0].degree, "Bachelor of Technology (B.Tech)")
        self.assertEqual(edu_list[0].major, "Computer Science")
        self.assertEqual(edu_list[0].gpa, "9.2/10")

        self.assertEqual(edu_list[1].institution, "Stanford University")
        self.assertEqual(edu_list[1].dates, "2021 - 2023")
        self.assertEqual(edu_list[1].degree, "Master of Science")
        self.assertEqual(edu_list[1].major, "Artificial Intelligence")
        self.assertEqual(edu_list[1].gpa, "3.8/4.0")

    def test_experience_timeline_parsing(self):
        """Verify experience timeline parses roles, companies, durations, achievements, and tech."""
        exp_text = """IBM Software Engineer
        2024 - Present
        • Built scalable backend API frameworks using Python.
        • Collaborated in a structured engineering sprint context.
        """
        intern_text = """Tata iQ Data Scientist Intern
        Aug 2025
        • Conducted ML deliquency analytics using PyTorch.
        """
        exp_list = _parse_experience_blocks(exp_text, intern_text)
        self.assertEqual(len(exp_list), 2)

        self.assertEqual(exp_list[0].company, "IBM")
        self.assertEqual(exp_list[0].title, "Software Engineer")
        self.assertEqual(exp_list[0].duration, "2024 - Present")
        self.assertIn("Python", exp_list[0].technologies)
        self.assertEqual(len(exp_list[0].achievements), 2)
        self.assertEqual(exp_list[0].achievements[0], "Built scalable backend API frameworks using Python.")

        self.assertEqual(exp_list[1].company, "Tata")
        self.assertEqual(exp_list[1].title, "Data Scientist Intern")
        self.assertEqual(exp_list[1].duration, "Aug 2025")
        self.assertIn("PyTorch", exp_list[1].technologies)
        self.assertEqual(len(exp_list[1].achievements), 1)

    def test_project_intelligence_parsing(self):
        """Verify project timeline extracts tech stacks, URLs, domains, and achievements."""
        text = """AI Screening System
        • Developed a similarity matching tool using NLP and TensorFlow.
        • Project source code: https://github.com/example/screening
        • Live application demo: https://screening.app
        """
        projects = _parse_project_blocks(text)
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].title, "AI Screening System")
        self.assertIn("TensorFlow", projects[0].technologies)
        self.assertEqual(projects[0].domain, "Artificial Intelligence")
        self.assertEqual(projects[0].github, "https://github.com/example/screening")
        self.assertEqual(projects[0].demo, "https://screening.app")
        self.assertEqual(len(projects[0].key_achievements), 3)

    def test_certification_intelligence_parsing(self):
        """Verify certifications mapping organization names and verification structures."""
        text = "IBM ML Specialization • AWS Cloud Practitioner • Google Cloud Architect"
        certs = _parse_certification_blocks(text)
        self.assertEqual(len(certs), 3)
        self.assertEqual(certs[0].organization, "IBM")
        self.assertEqual(certs[1].organization, "AWS")
        self.assertEqual(certs[2].organization, "Google")

    @patch("modules.parser.preprocess_file")
    def test_candidate_narrative_fallback(self, mock_preprocess):
        """Verify narrative auto-generation compiles evidence-based summaries under 100 words."""
        mock_preprocess.return_value = {
            "text": "Jane Doe\nJane's contact details.",
            "sections": {
                "Education": "Stanford University\nExpected 2026\nB.S. in Computer Science",
                "Skills": "Python, Docker, SQL",
            }
        }
        # Parse fake file (path does not need to exist because preprocess is mocked)
        candidate = parse_resume(Path("jane_resume.pdf"))
        self.assertIn("Jane Doe", candidate.summary)
        self.assertIn("Python", candidate.summary)
        self.assertIn("Stanford University", candidate.summary)
        self.assertLess(len(candidate.summary.split()), 100)

    @patch("modules.parser.preprocess_file")
    def test_edge_case_empty_sections(self, mock_preprocess):
        """Verify empty and missing section arrays are parsed gracefully without exceptions."""
        mock_preprocess.return_value = {
            "text": "Empty candidate text block",
            "sections": {}
        }
        candidate = parse_resume(Path("empty.pdf"))
        self.assertEqual(candidate.contact.name, "Empty candidate text block")
        self.assertEqual(len(candidate.experience), 0)
        self.assertEqual(len(candidate.education), 0)
        self.assertEqual(len(candidate.projects), 0)
        self.assertEqual(len(candidate.certifications), 0)

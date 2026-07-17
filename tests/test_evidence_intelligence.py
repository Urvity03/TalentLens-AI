"""Unit tests for the Evidence Intelligence classifier, grouping engine, and immutability."""

from dataclasses import FrozenInstanceError
import unittest

from modules.models import (
    CandidateProfile,
    Certification,
    ContactInfo,
    Education,
    EvidenceCategory,
    Experience,
    Project,
    Skill,
    ProfessionalIdentity,
    TechnicalProfile,
)
from modules.evidence_intelligence import compile_evidence_collection


class TestEvidenceIntelligence(unittest.TestCase):
    """Test suite validating Evidence Intelligence grouping, traceability, and immutability."""

    def setUp(self):
        """Construct a sample CandidateProfile (Resume) with realistic data."""
        self.profile = CandidateProfile(
            contact=ContactInfo(name="Jane Doe", email="jane@doe.com"),
            summary="Experienced engineer with Python expertise.",
            skills=[
                Skill("Python"),
                Skill("FastAPI"),
                Skill("PostgreSQL"),
                Skill("AWS"),
                Skill("TensorFlow"),
                Skill("Teamwork"),
                Skill("UnknownTechCredential"),
            ],
            experience=[
                Experience(
                    description="Led development of scalable Python systems.\nMentored 4 engineers.",
                    title="Senior Backend Lead",
                    company="Vercel",
                    duration="2023 - Present",
                    technologies=["Python", "FastAPI"],
                    achievements=["Led development of scalable systems.", "Mentored 4 engineers."],
                ),
                Experience(
                    description="Served as Data Scientist Intern.\nConducted NLP analytics.",
                    title="Data Scientist Intern",
                    company="IBM",
                    duration="2022 - 2023",
                    technologies=["TensorFlow"],
                    achievements=["Conducted NLP analytics."],
                ),
                Experience(
                    description="Worked as Freelance Web Developer contract.",
                    title="Freelance Developer",
                    company="Upwork",
                    duration="2021",
                    technologies=["JavaScript"],
                    achievements=["Built contract web apps."],
                ),
            ],
            education=[
                Education(
                    description="Bachelor of Technology in CS. Coursework: Databases, ML.",
                    degree="Bachelor of Technology",
                    institution="MIT",
                    dates="2018 - 2022",
                    major="Computer Science",
                    gpa="3.9/4.0",
                )
            ],
            projects=[
                Project(
                    description="Deployed distributed data pipeline using GPU optimization.",
                    title="Distributed Analytics",
                    technologies=["Python", "GPU"],
                    domain="Artificial Intelligence",
                    github="https://github.com/jane/dist-analytics",
                    demo="https://analytics.demo.app",
                ),
                Project(
                    description="Academic research thesis on NLP algorithms.",
                    title="NLP Thesis",
                    technologies=["Python"],
                    domain="Artificial Intelligence",
                ),
            ],
            certifications=[
                Certification(
                    description="IBM ML Badge",
                    name="IBM Machine Learning Specialization",
                    organization="IBM",
                ),
                Certification(
                    description="General Cloud Competency",
                    name="Certified Cloud Associate",
                    organization="CloudOrg",
                ),
            ],
            professional_identity=ProfessionalIdentity(
                current_title="Senior Backend Lead",
                career_focus="Backend Engineering",
                primary_domain="Software Engineering",
                technical_specialization="Backend Systems",
            ),
            technical_profile=TechnicalProfile(
                programming_languages=["Python"],
                frameworks=["FastAPI"],
                libraries=[],
                databases=["PostgreSQL"],
                cloud=["AWS"],
                developer_tools=[],
                ml_tools=["TensorFlow"],
                soft_skills=["Teamwork"],
            ),
        )

    def test_technical_evidence_categories_and_uncategorized(self):
        """Verify TechnicalEvidence groups skills correctly and preserves unknown skills."""
        collection = compile_evidence_collection(self.profile)
        tech = collection.technical

        # Verify category items lists
        langs = [item.content for item in tech.programming_languages]
        self.assertIn("Python", langs)
        self.assertEqual(tech.programming_languages[0].category, EvidenceCategory.TECHNICAL)
        self.assertEqual(tech.programming_languages[0].source.section, "Skills")

        frameworks = [item.content for item in tech.frameworks]
        self.assertIn("FastAPI", frameworks)

        databases = [item.content for item in tech.databases]
        self.assertIn("PostgreSQL", databases)

        cloud = [item.content for item in tech.cloud]
        self.assertIn("AWS", cloud)

        ml = [item.content for item in tech.ml_tools]
        self.assertIn("TensorFlow", ml)

        soft = [item.content for item in tech.soft_skills]
        self.assertIn("Teamwork", soft)

        # Uncategorized preservation
        uncat = [item.content for item in tech.uncategorized]
        self.assertIn("UnknownTechCredential", uncat)

    def test_experience_evidence_grouping(self):
        """Verify ExperienceEvidence groups leadership, internships, and freelance/contract work."""
        collection = compile_evidence_collection(self.profile)
        exp = collection.experience

        # Relevant roles
        self.assertEqual(len(exp.relevant_roles), 3)

        # Leadership indicators
        leaders = [item.content for item in exp.leadership_indicators]
        self.assertEqual(len(leaders), 1)
        self.assertIn("Backend Lead", leaders[0])
        self.assertEqual(exp.leadership_indicators[0].source.block_index, 0)

        # Internships
        interns = [item.content for item in exp.internships]
        self.assertEqual(len(interns), 1)
        self.assertIn("Intern", interns[0])
        self.assertEqual(exp.internships[0].source.block_index, 1)

        # Freelance or contract
        contracts = [item.content for item in exp.freelance_or_contract]
        self.assertEqual(len(contracts), 1)
        self.assertIn("Freelance", contracts[0])

    def test_project_evidence_grouping(self):
        """Verify ProjectEvidence groups deployed, academic, and complexity items."""
        collection = compile_evidence_collection(self.profile)
        proj = collection.project

        # Production / Deployed check
        self.assertEqual(len(proj.production_or_deployed), 1)
        self.assertIn("Distributed Analytics", proj.production_or_deployed[0].content)

        # Academic / Research check
        self.assertEqual(len(proj.academic_or_research), 1)
        self.assertIn("NLP Thesis", proj.academic_or_research[0].content)

        # Complexity check (mentions deployed, distributed, gpu, optimization keywords)
        self.assertEqual(len(proj.complexity_indicators), 1)
        self.assertIn("distributed", proj.complexity_indicators[0].tags)
        self.assertIn("gpu", proj.complexity_indicators[0].tags)

    def test_education_evidence_gpa_and_coursework(self):
        """Verify EducationEvidence extracts degrees, coursework references, and GPA score cards."""
        collection = compile_evidence_collection(self.profile)
        edu = collection.education

        self.assertEqual(len(edu.degrees), 1)
        self.assertIn("MIT", edu.degrees[0].content)

        self.assertEqual(len(edu.coursework), 1)
        self.assertIn("MIT", edu.coursework[0].content)

        self.assertEqual(len(edu.performance_markers), 1)
        self.assertIn("3.9/4.0", edu.performance_markers[0].content)

    def test_certification_evidence_vendor_vs_industry(self):
        """Verify CertificationEvidence separates vendor credentials from industry associates."""
        collection = compile_evidence_collection(self.profile)
        cert = collection.certification

        self.assertEqual(len(cert.vendor_certifications), 1)
        self.assertIn("IBM", cert.vendor_certifications[0].content)

        self.assertEqual(len(cert.industry_certifications), 1)
        self.assertIn("CloudOrg", cert.industry_certifications[0].content)

    def test_resume_evidence_metrics_and_action_verbs(self):
        """Verify ResumeEvidence extracts metrics, percentage patterns, and strong active statements."""
        collection = compile_evidence_collection(self.profile)
        res = collection.resume

        # Metrics check (e.g. "4 engineers")
        metrics = [item.content for item in res.metrics]
        self.assertEqual(len(metrics), 1)
        self.assertIn("4 engineers", metrics[0])

        # Action verbs check (e.g. starting with Led, Served, Worked)
        verbs = [item.content for item in res.action_verbs]
        self.assertEqual(len(verbs), 5)

    def test_source_traceability_preservation(self):
        """Verify that every EvidenceItem holds deterministic tags and valid EvidenceSource markers."""
        collection = compile_evidence_collection(self.profile)
        item = collection.technical.programming_languages[0]

        self.assertIsNotNone(item.id)
        self.assertEqual(item.category, EvidenceCategory.TECHNICAL)
        self.assertIn("languages", item.tags)
        self.assertEqual(item.source.section, "Skills")
        self.assertEqual(item.source.block_index, 0)
        self.assertEqual(item.source.raw_text, "Python")

    def test_immutability_enforcements(self):
        """Verify that EvidenceCollection, items, and sources raise FrozenInstanceError on mutations."""
        collection = compile_evidence_collection(self.profile)

        # Attempting mutation on the root collection
        with self.assertRaises(FrozenInstanceError):
            collection.technical = None

        # Attempting mutation on individual category models
        with self.assertRaises(FrozenInstanceError):
            collection.technical.programming_languages = ()

        # Attempting mutation on evidence item attributes
        with self.assertRaises(FrozenInstanceError):
            collection.technical.programming_languages[0].content = "NewSkill"

    def test_determinism_identical_runs(self):
        """Verify that compile_evidence_collection is a pure deterministic transformation."""
        collection_1 = compile_evidence_collection(self.profile)
        collection_2 = compile_evidence_collection(self.profile)

        self.assertEqual(collection_1, collection_2)

    def test_edge_case_empty_candidate(self):
        """Verify that empty candidate timelines yield empty collections without raising exceptions."""
        empty_profile = CandidateProfile()
        collection = compile_evidence_collection(empty_profile)

        self.assertEqual(len(collection.technical.programming_languages), 0)
        self.assertEqual(len(collection.experience.relevant_roles), 0)
        self.assertEqual(len(collection.project.production_or_deployed), 0)
        self.assertEqual(len(collection.education.degrees), 0)
        self.assertEqual(len(collection.certification.vendor_certifications), 0)

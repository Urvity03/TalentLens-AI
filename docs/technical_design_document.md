# TalentLens AI - Technical Design Document (TDD)
## Version: 1.0.0
## Category: AI Hiring Intelligence Platform
## Status: Approved / Production Blueprint
## Author: Technical Lead & Chief Architect, TalentLens AI Group

---

## 1. Executive Summary

### System Purpose
TalentLens AI is an enterprise-grade AI Hiring Intelligence Platform designed to automate and standardize candidate pre-screening. It parses unstructured resume documents, performs semantic similarity mapping against job descriptions, identifies skill matches and gaps, projects career development roadmaps, and compiles structured recruiter insights.

### High-Level Architecture
The system follows a clean, layered architecture with unidirectional data flow. The user interface layer remains decoupled from business logic. The application core coordinates execution through dedicated services, routing raw data to single-responsibility intelligence modules. Output data structures are enforced through type-safe domain models.

### Engineering Philosophy
Our architecture is built on predictability, testability, and explainability. We avoid "black-box" models, ensuring that every AI score is supported by clear evidence.

### Scalability Goals
- **Throughput**: Single candidate screening execution must run in <0.5 seconds (post model cache initialization).
- **Concurrency**: The core orchestration layers must remain stateless to support horizontal scaling across isolated container nodes.
- **Resource Footprint**: Memory usage per evaluation request must be optimized, keeping memory footprints low.

### Maintainability Goals
- **Strict Loose Coupling**: The UI layer can be replaced (e.g. migrating from a dashboard framework to a FastAPI REST server) without editing parsing, similarity, or intelligence modules.
- **Test Coverage**: Maintain a minimum test coverage of 90% across core intelligence modules.

---

## 2. System Architecture

The execution pipeline flows unidirectionally from the presentation layer to the core domain services:

```
                  ┌─────────────────────────────────────────┐
                  │          Recruiter UI Shell             │
                  └────────────────────┬────────────────────┘
                                       │ Uploads & Settings
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │          UI Component Layer             │
                  └────────────────────┬────────────────────┘
                                       │ Native Parameters
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │      Services Orchestration Layer       │
                  └────────────────────┬────────────────────┘
                                       │ Execution Pipeline
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │         AI Intelligence Engine          │
                  └──────────┬───────────────────┬──────────┘
                             │                   │
      ┌──────────────────────▼───────┐   ┌───────▼──────────────────────┐
      │  Candidate Intel. Module     │   │  Skill Intel. Module         │
      ├──────────────────────────────┤   ├──────────────────────────────┤
      │  Experience Intel. Module    │   │  Project Intel. Module       │
      ├──────────────────────────────┤   ├──────────────────────────────┤
      │  Resume Intel. Module        │   │  Education Intel. Module     │
      ├──────────────────────────────┤   ├──────────────────────────────┤
      │  Certification Intel.        │   │  Risk Intel. Module          │
      └──────────────────────────────┘   └──────────────────────────────┘
                             │                   │
                             └─────────┬─────────┘
                                       │ Structured Scores & Indicators
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │               AHRI Engine               │
                  └────────────────────┬────────────────────┘
                                       │ Grade Mappings & Verdicts
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │          Decision Engine (PDF)          │
                  └─────────────────────────────────────────┘
```

- **Recruiter UI Shell**: The primary entry point for recruiters to configure uploads and toggle options.
- **UI Component Layer**: Contains modular navbar, sidebar, card, and chart components.
- **Services Orchestration Layer**: Orchestrates the analysis pipeline, managing file validation and temporary storage.
- **AI Intelligence Engine**: Cohesive intelligence modules evaluating candidate characteristics.
- **AHRI Engine**: Compiles scores from the intelligence layers into a composite letter grade.
- **Decision Engine (PDF)**: Generates structured, print-ready candidate evaluation reports.

---

## 3. Engineering Principles

- **Single Responsibility (SRP)**: Each module performs one function. The parser extracts text, the similarity engine calculates semantic scores, and the roadmap engine maps developmental steps.
- **Loose Coupling**: Components communicate via structured dataclasses, allowing you to swap UI frameworks or parsing engines without affecting other layers.
- **High Cohesion**: Related logic is kept together. All Plotly charts are grouped in `ui/charts.py`, and all scoring formulas are in `modules/ahri.py`.
- **Dependency Injection**: Dependencies are passed into functions rather than initialized inside them.
- **Composition over Inheritance**: We build composite objects (e.g. `AnalysisResult` containing instances of `Resume` and `AHRIResult`) rather than using deep inheritance hierarchies.
- **Explainability**: Every score must be supported by clear evidence, such as matched skills list, strengths, and concern logs.
- **SOLID, DRY, KISS, YAGNI**: We prioritize simple, maintainable code, avoiding unnecessary optimizations or features.

---

## 4. Folder Structure

```
TalentLens-AI/
 ├── docs/                             # Engineering specs and PRDs
 ├── assets/                           # Brand assets and graphics
 ├── config/                           # Application configuration files
 ├── ui/                               # Presentation layer components
 │    ├── theme.py                     # Light/Dark design tokens
 │    ├── styles.py                    # Global stylesheet injections
 │    ├── cards.py                     # Reusable layout cards
 │    ├── charts.py                    # Plotly chart configurations
 │    ├── navbar.py                    # Platform header layout
 │    ├── sidebar.py                   # Recruitment control panel
 │    └── export_pdf.py                # PDF document generator
 ├── services/                         # Pipeline orchestration
 │    └── analyzer.py                  # Core analysis pipeline orchestrator
 ├── modules/                          # AI and calculations core
 │    ├── models.py                    # Type-safe domain schemas
 │    ├── preprocess.py                # Text extraction and ligature cleaning
 │    ├── parser.py                    # Resume section parsing
 │    ├── jd_parser.py                 # Job description parsing
 │    ├── skill_extractor.py           # RegEx skill matcher
 │    ├── skill_intelligence.py        # Skill match percentage calculations
 │    ├── similarity.py                # Semantic similarity mapping
 │    ├── ahri.py                      # AHRI v2.0 composite scoring
 │    ├── quality_score.py             # Resume layout completeness scoring
 │    ├── potential_predictor.py       # Candidate potential prediction
 │    ├── recruiter_insights.py        # Strengths and concerns generator
 │    └── roadmap.py                   # Career roadmap generation
 ├── tests/                            # Comprehensive test suites
 └── requirements.txt                  # Python dependencies
```

---

## 5. Module Responsibilities

- **`modules/preprocess.py`**: Extracts text from PDF and DOCX documents and normalizes spacing and ligatures.
- **`modules/parser.py`**: Segment resume blocks into structured data fields.
- **`modules/jd_parser.py`**: Extracts titles, skills, and required experience from job descriptions.
- **`modules/skill_extractor.py`**: Matches text against a predefined list of technical skills.
- **`modules/skill_intelligence.py`**: Calculates matched vs. missing skills and match percentage ratios.
- **`modules/similarity.py`**: Compares resumes and job descriptions using SentenceTransformer embeddings.
- **`modules/ahri.py`**: Computes the composite readiness score and letter grade.
- **`modules/potential_predictor.py`**: Forecasts candidate growth potential.
- **`modules/recruiter_insights.py`**: Generates recruiter summaries detailing strengths and concerns.
- **`modules/roadmap.py`**: Compiles career roadmaps for candidates with skill gaps.
- **`ui/export_pdf.py`**: Generates a standard candidate evaluation report PDF using Helvetica.
- **`services/analyzer.py`**: Manages the execution flow of the analysis pipeline.

---

## 6. Data Models

We enforce domain schemas using structured dataclasses:

- **`ContactInfo`**: Candidate contact details.
- **`Skill`**: Skill name and extraction confidence.
- **`Experience`**: Previous job title, company, and description.
- **`Education`**: Degree, institution, and description.
- **`Project`**: Project title and description.
- **`Certification`**: Certification name and description.
- **`Resume`**: Candidate profile containing contact, summary, skills, experience, education, projects, and certifications.
- **`JobDescription`**: Target role parameters containing title, summary, skills, experience, and education.
- **`SimilarityResult`**: Semantic similarity scores for summary, skills, and experience.
- **`AHRIResult`**: Composite readiness score, letter grade, strengths, missing skills, and recommendations.
- **`SkillIntelligence`**: Lists of matched vs. missing skills and match percentage.
- **`PotentialPrediction`**: Predicted growth score and level.
- **`RecruiterInsights`**: Highlighted strengths, concerns, and verdict recommendation.
- **`CareerRoadmap`**: Career roadmap steps.
- **`AnalysisResult`**: The root dashboard object packaging all pipeline analysis outputs.

---

## 7. Data Flow

```
[Resume Upload (PDF/DOCX) + JD (Paste/File)]
                    │
                    ▼
          [services/analyzer.py]
                    │
                    ├─► [modules/preprocess.py] ── (Extracts and normalizes text)
                    │
                    ├─► [modules/parser.py] ────── (Segments data sections)
                    │
                    ├─► [modules/similarity.py] ── (Computes semantic similarity)
                    │
                    ├─► [modules/ahri.py] ──────── (Calculates composite scores)
                    │
                    └─► [modules/roadmap.py] ───── (Generates developmental steps)
                    │
                    ▼
          [AnalysisResult Payload]
                    │
                    ├─► [ui/cards.py & ui/charts.py] (Renders dashboard panels)
                    │
                    └─► [ui/export_pdf.py] ────────── (Compiles report PDF)
```

---

## 8. AI Intelligence Engine
The **AI Intelligence Engine** evaluates candidate fit across several core dimensions:
- **Candidate Intelligence**: Maps and validates candidate contact details.
- **Skill Intelligence**: Normalizes skills and maps matches and gaps.
- **Experience Intelligence**: Evaluates career progression and job descriptions.
- **Project Intelligence**: Analyzes the complexity and relevance of candidate projects.
- **Resume Intelligence**: Evaluates the formatting and completeness of the resume.
- **Education Intelligence**: Evaluates academic alignment, ignoring school brand names.
- **Certification Intelligence**: Validates and maps candidate certifications.
- **Risk Intelligence**: Highlights significant experience gaps or short job tenures.

---

## 9. AHRI Integration
The composite readiness score (AHRI) combines the outputs of the intelligence layers:

- **Base Similarity**: Calculated as a weighted sum of summary (20%), skills (50%), and experience (30%) similarities.
- **Bonus Score**: Adds up to 10 points for matching skills.
- **Penalty Score**: Deducts up to 10 points for missing required skills.
- **Grade Assignment**: Maps scores to letter grades (A+ to F).

---

## 10. Recommendation Engine
The platform generates hiring recommendations using rules-based logic:
- **Decision Logic**: Suggests candidate progression based on AHRI scores and quality metrics.
- **Verdicts**: Mapped to "Fast-Track", "Standard Screen", or "Upskilling Route" recommendations.
- **Evidence Ledger**: Supports every recommendation with a detailed breakdown of candidate strengths and concerns.

---

## 11. Error Handling Strategy
- **Corrupt PDFs / Invalid Formats**: The system catches file extraction errors and presents a clear error message in the UI, cleaning up temporary files.
- **Empty Sections**: Fallback summaries are generated if a resume or job description is missing a summary section.
- **Missing Skills**: If a job description lacks structured skills, the system shifts to a semantic comparison, warning the recruiter in the dashboard.

---

## 12. Logging Strategy
- **Application Logs**: Logs workflow events (file uploads, page refresh events).
- **Parser Logs**: Tracks text extraction results, normalization steps, and section detection.
- **AI Logs**: Logs SentenceTransformer initialization events, embedding shapes, and execution latency.
- **Security Audit Logs**: Logs file upload attempts, file sizes, and verification outcomes.

---

## 13. Configuration Strategy
- **Centralized Constants**: Weights, grades, patterns, and model directories are defined in `modules/config.py`.
- **Environment Variables**: We utilize environment variables for things like API keys, model paths, and feature flags.

---

## 14. Performance Strategy
- **Model Caching**: The SentenceTransformer model is cached in-memory to prevent initialization delays on subsequent runs.
- **Document Cleanups**: Temporary files are cleaned up securely using `finally` blocks, preventing memory leaks.
- **Lazy Loading**: Visual assets and charts are loaded lazily to keep the dashboard responsive.

---

## 15. Security Strategy
- **Input Sanitization**: File uploads are restricted to supported extensions (PDF, DOCX, TXT) and checked for size limits.
- **Data Isolation**: PII fields (names, locations, contact info) are excluded from semantic embeddings.
- **Secure File Cleanups**: Temporary files are deleted immediately after evaluation.

---

## 16. Testing Strategy
- **Unit Tests**: Test core calculation layers, scoring formulas, and parsing utilities.
- **Integration Tests**: Verify the execution flow of the analysis pipeline.
- **Golden Dataset**: Benchmarks the model against human recruiter ratings, targetting a Pearson correlation of $r \ge 0.85$.
- **Regression Tests**: Automated tests verify that code changes do not impact scoring consistency or break PDF exports.

---

## 17. Extensibility
The platform is designed to support future scaling:
- **REST API Support**: The services orchestration layer can be wrapped in a FastAPI REST engine without refactoring.
- **Database Persistence**: Dataclass payloads can be serialized directly to JSON or stored in PostgreSQL databases.
- **Vector Database Integrations**: We can integrate vector databases (e.g. PgVector, Pinecone) for candidate sourcing search.
- **ATS Webhooks**: We can add webhooks to push assessment outcomes to ATS tools (Ashby, Greenhouse, Lever).

---

## 18. Release Strategy
- **V1.0 MVP**: Single candidate evaluation cockpit with 6-tab analytics dashboard and fitz PDF export.
- **V2.0 Batch Mode**: Adds bulk upload support, multi-candidate ranking tables, and custom interview guides.
- **V3.0 Ecosystem**: Adds candidate self-serve upskilling views and third-party ATS connectors.

---

## 19. Technical Debt Policy
- **Acceptable Debt**: Compatibility wrappers to bridge old test suites, prototype recommendations lists, and hardcoded config limits.
- **Forbidden Debt**: Duplicated business logic, inline HTML styles, and hardcoded PDF layouts without buffer overflow checks.

---

## 20. Definition of Done
A feature is complete only if:
- The design meets the TDD architecture standards.
- Unit tests cover all code paths and pass successfully.
- Code matches DRY principles and has no duplication.
- UI components are integrated, responsive, and accessible.
- Documentation and specification blueprints are updated.

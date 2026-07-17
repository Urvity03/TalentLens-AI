# TalentLens AI - Milestone 3 Implementation Plan: Risk Intelligence
## Version: 1.0.0
## Category: Engineering Roadmap
## Status: Pending Approval
## Author: Lead Software Architect & Staff AI Engineer, TalentLens AI Group

---

## 1. Audit of Current Implementation

We compared the active codebase against the specifications for **Milestone 3 (Risk Intelligence)**:

| Risk Dimension | Current Behavior | Missing / Needs Improvement |
| :--- | :--- | :--- |
| **1. Experience Gaps** | None. | **Missing**: Analyzing candidate experience duration intervals for gaps > 6 months. |
| **2. Job Tenure Turnover** | None. | **Missing**: Calculating average job tenure and flagging candidates with multiple short tenures (< 1 year). |
| **3. Critical Skills Gaps** | Flat list of missing skills compiled during similarity matching. | **Needs Improvement**: Classifying missing skills into critical/mandatory gaps based on requirements. |
| **4. Credentials Validation Risks** | None. | **Missing**: Flagging unverified or missing certifications for regulated domains. |
| **5. Structured Risk Model** | Static list of string warnings in `RecruiterInsights`. | **Missing**: Immutable, structured `RiskAssessment` dataclass with traceability to `EvidenceCollection`. |

---

## 2. Technical Design & Architecture

### New Dataclasses (`modules/models.py`)
To preserve immutability and type safety, we will define the following models:
```python
@dataclass(frozen=True)
class RiskIndicator:
    """A single identified risk flag."""
    id: str
    label: str
    description: str
    severity: str  # "LOW", "MEDIUM", "HIGH"
    evidence_id: str | None  # Trace back to specific EvidenceItem

@dataclass(frozen=True)
class RiskAssessment:
    """Consolidated immutable risk profile for the candidate."""
    experience_gaps: tuple[RiskIndicator, ...]
    turnover_risk: tuple[RiskIndicator, ...]
    skills_mismatch: tuple[RiskIndicator, ...]
    unverified_credentials: tuple[RiskIndicator, ...]
```

### New Module (`modules/risk_intelligence.py`)
Exposes exactly one public function:
```python
def assess_candidate_risk(
    profile: CandidateProfile,
    evidence: EvidenceCollection,
    job_description: JobDescription,
) -> RiskAssessment
```
All sub-assessments remain private helper functions:
- `_assess_experience_gaps()`
- `_assess_turnover_patterns()`
- `_assess_skills_mismatches()`
- `_assess_credential_risks()`

---

## 3. Files Requiring Modification

1. [`modules/models.py`](file:///C:/Users/ASUS/OneDrive/Documents/GitHub/TalentLens-AI/modules/models.py)
   - *Why*: Needs to define the `RiskAssessment` and `RiskIndicator` models.
2. [`modules/risk_intelligence.py`](file:///C:/Users/ASUS/OneDrive/Documents/GitHub/TalentLens-AI/modules/risk_intelligence.py) (New)
   - *Why*: Holds all risk rules, gap checks, and tenure calculations.
3. [`services/analyzer.py`](file:///C:/Users/ASUS/OneDrive/Documents/GitHub/TalentLens-AI/services/analyzer.py)
   - *Why*: Integrates risk assessment into the orchestrator pipeline.

---

## 4. Implementation Steps

- **Step 1**: Write `RiskAssessment` schemas to `modules/models.py`.
- **Step 2**: Create `modules/risk_intelligence.py` with date parsing and tenure calculations.
- **Step 3**: Write tests in `tests/test_risk_intelligence.py` verifying gap thresholds.
- **Step 4**: Integrate as an internal execution artifact in `services/analyzer.py`.

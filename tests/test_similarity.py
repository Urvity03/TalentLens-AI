"""Test the semantic similarity engine."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from modules.jd_parser import parse_job_description
from modules.parser import parse_resume
from modules.similarity import calculate_resume_similarity


resume = parse_resume(
    "samples/resumes/sample_resume.pdf"
)

job = parse_job_description(
    "samples/job_descriptions/sample_jd.txt"
)

result = calculate_resume_similarity(
    resume,
    job,
)

print(result)

assert 0 <= result.summary <= 100
assert 0 <= result.skills <= 100
assert 0 <= result.experience <= 100
assert 0 <= result.overall <= 100

print("\n✅ Similarity Engine Working!")
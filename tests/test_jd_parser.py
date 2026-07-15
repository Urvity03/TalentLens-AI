"""Simple tests for job description parsing."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from modules.jd_parser import parse_job_description


sample_path = PROJECT_ROOT / "samples" / "job_descriptions" / "sample_jd.txt"
jd = parse_job_description(sample_path)

print(jd)

assert jd.title == "Machine Learning Engineer"
assert jd.summary
assert len(jd.skills) > 0
assert jd.experience
assert jd.education

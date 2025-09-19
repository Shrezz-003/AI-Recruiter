# File: app/services/jd_parser.py
from app.services.resume_parser import extract_skills

def parse_job_description(description: str):
    # We can reuse the same skill extractor we built for resumes!
    return extract_skills(description)
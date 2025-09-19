# File: app/api/jobs.py
from fastapi import APIRouter
from app.schemas.job import JobDescription
from app.services import jd_parser

router = APIRouter()

@router.post("/jobs/parse-jd")
def parse_jd_endpoint(job_desc: JobDescription):
    skills = jd_parser.parse_job_description(job_desc.description)
    return {"job_title": job_desc.title, "extracted_skills": skills}
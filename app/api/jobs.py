# File: app/api/jobs.py
from fastapi import APIRouter
from app.schemas.job import JobDescription
from app.services import jd_parser
from app.services import matching_service
from app.core.vector_db import index

router = APIRouter()

@router.post("/jobs/parse-jd")
def parse_jd_endpoint(job_desc: JobDescription):
    skills = jd_parser.parse_job_description(job_desc.description)
    return {"job_title": job_desc.title, "extracted_skills": skills}

@router.post("/jobs/{job_id}/find-matches")
def find_matches_for_job(job_id: int, top_k: int = 5):
    # In a real app, you'd fetch the job's skills from your database
    # For now, let's use a hardcoded example list of JD skills
    jd_skills = ["python", "fastapi", "docker", "machine learning", "aws"]

    # 1. Generate a single vector for the entire job description's skill set
    jd_embedding = matching_service.model.encode(jd_skills).tolist()

    # 2. Query Pinecone to find the top_k most similar resume vectors
    query_response = index.query(
        vector=jd_embedding,
        top_k=top_k,
        include_metadata=True
    )

    matches = query_response['matches']
    return {"job_id": job_id, "matches": matches}
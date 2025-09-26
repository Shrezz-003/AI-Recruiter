from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import List
from app.services import text_extractor, resume_parser, matching_service, question_generator, pdf_generator
import re

router = APIRouter()


# This is your existing endpoint for sorting
@router.post("/sort-resumes")
async def sort_resumes(
        job_description_str: str = Form(...),
        resumes: List[UploadFile] = File(...)
):
    if len(resumes) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Minimum of 10 resumes must be uploaded."
        )

    jd_skills = resume_parser.extract_skills(job_description_str)
    sorted_candidates = []

    for resume_file in resumes:
        raw_text = text_extractor.extract_text(resume_file)
        if not raw_text:
            continue

        resume_skills = resume_parser.extract_skills(raw_text)
        score = matching_service.calculate_fit_score(resume_skills, jd_skills)

        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', raw_text)
        email = email_match.group(0) if email_match else "Not found"

        sorted_candidates.append({
            "filename": resume_file.filename,
            "email": email,
            "fit_score_percent": score
        })

    sorted_candidates.sort(key=lambda x: x['fit_score_percent'], reverse=True)
    return {"sorted_candidates": sorted_candidates}


# --- NEW ENDPOINTS FOR INTERVIEW KIT ---

def get_interview_kit_data(candidate_id: int):
    """Helper function to generate mock data. In a real app, this would fetch
    data from your database for a specific candidate and job."""

    job_skills = ["Python", "FastAPI", "Docker", "AWS", "SQL"]
    ai_questions_data = question_generator.generate_interview_questions(job_skills)

    return {
        "candidate_id": candidate_id,
        "candidate_email": f"candidate_{candidate_id}@example.com",
        "fit_score": 85.5,
        "matched_skills": ["Python", "FastAPI", "Docker"],
        "missing_skills": ["AWS", "SQL"],
        "questions": ai_questions_data.get("questions", [])
    }


# ENDPOINT 1: Get Interview Kit data as JSON for the web page
@router.get("/interview-kit/{candidate_id}", tags=["Interview Kit"])
def get_interview_kit_json(candidate_id: int):
    kit_data = get_interview_kit_data(candidate_id)
    return kit_data


# ENDPOINT 2: Generate and download the Interview Kit as a PDF
@router.get("/interview-kit/{candidate_id}/download", tags=["Interview Kit"])
def download_interview_kit_pdf(candidate_id: int):
    kit_data = get_interview_kit_data(candidate_id)
    pdf_buffer = pdf_generator.create_interview_kit_pdf(kit_data)

    headers = {'Content-Disposition': f'attachment; filename="interview_kit_{candidate_id}.pdf"'}
    return StreamingResponse(pdf_buffer, headers=headers, media_type='application/pdf')
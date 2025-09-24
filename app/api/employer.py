from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from typing import List
from app.services import text_extractor, resume_parser, matching_service, question_generator
import json

router = APIRouter()


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

        # A simple regex can be used to find emails, but a more robust solution
        # would be needed for a real app.
        import re
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', raw_text)
        email = email_match.group(0) if email_match else "Not found"

        sorted_candidates.append({
            "filename": resume_file.filename,
            "email": email,
            "fit_score_percent": score
        })

    # Sort in descending order of fit score
    sorted_candidates.sort(key=lambda x: x['fit_score_percent'], reverse=True)

    return {"sorted_candidates": sorted_candidates}


@router.post("/ask-questions")
def ask_questions(job_description: str, fields: List[str]):
    # In this context, 'fields' are interpreted as specific skills to focus on
    # Generate questions aligned with the specified fields/skills
    questions = question_generator.generate_interview_questions(fields)
    return questions
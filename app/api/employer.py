from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from typing import List
from app.services import text_extractor, pdf_generator, ai_recruiter_service
from app.api import deps
from app.models.user import User
import re

router = APIRouter()


@router.post("/sort-resumes")
async def sort_resumes(
        job_description_str: str = Form(...),
        resumes: List[UploadFile] = File(...),
        current_user: User = Depends(deps.get_current_user)
):
    if len(resumes) < 1:  # Reduced for easier testing, can be increased later
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one resume must be uploaded."
        )

    analyzed_candidates = []

    for resume_file in resumes:
        raw_text = text_extractor.extract_text(resume_file)
        if not raw_text:
            continue

        # --- UPGRADE: Use the new intelligent service for analysis ---
        analysis = ai_recruiter_service.get_ai_match_analysis(
            job_description=job_description_str,
            resume_text=raw_text
        )

        # A simple regex to find emails for contact purposes
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', raw_text)
        email = email_match.group(0) if email_match else "Not found"

        candidate_profile = {
            "filename": resume_file.filename,
            "email": email,
            "analysis": analysis  # Store the entire rich analysis object
        }
        analyzed_candidates.append(candidate_profile)

    # Sort candidates in descending order based on the AI's fit score
    analyzed_candidates.sort(key=lambda x: x['analysis'].get('fit_score_percent', 0), reverse=True)

    return {"sorted_candidates": analyzed_candidates}


# --- UPGRADE: Interview Kit now uses the AI analysis ---
def get_interview_kit_data(candidate_id: int):
    # This is mock data. In a real app, you'd fetch a saved analysis from the DB.
    mock_analysis = {
        "fit_score_percent": 92,
        "skills_analysis": [
            {"skill": "Python", "possessed": "Yes"},
            {"skill": "FastAPI", "possessed": "Yes"},
            {"skill": "AWS", "possessed": "Partial"}
        ],
        "strengths": [
            "Extensive experience with Python and building scalable APIs.",
            "Demonstrated ability to work with cloud services."
        ],
        "weaknesses": [
            "Lacks direct experience with Kubernetes.",
            "Could elaborate more on database optimization techniques."
        ],
        "verdict": "Strongly Recommend Interview"
    }

    # Generate questions based on the AI's analysis of weaknesses/gaps
    skills_to_probe = [s['skill'] for s in mock_analysis['skills_analysis'] if s['possessed'] != 'Yes']
    ai_questions = ai_recruiter_service.question_generator.generate_interview_questions(skills_to_probe)

    return {
        "candidate_id": candidate_id,
        "candidate_email": f"candidate_{candidate_id}@example.com",
        "analysis": mock_analysis,
        "questions": ai_questions.get("questions", [])
    }


@router.get("/interview-kit/{candidate_id}", tags=["Interview Kit"])
def get_interview_kit_json(candidate_id: int, current_user: User = Depends(deps.get_current_user)):
    kit_data = get_interview_kit_data(candidate_id)
    return kit_data


@router.get("/interview-kit/{candidate_id}/download", tags=["Interview Kit"])
def download_interview_kit_pdf(candidate_id: int, current_user: User = Depends(deps.get_current_user)):
    kit_data = get_interview_kit_data(candidate_id)
    pdf_buffer = pdf_generator.create_interview_kit_pdf(kit_data)

    headers = {'Content-Disposition': f'attachment; filename="interview_kit_{candidate_id}.pdf"'}
    return StreamingResponse(pdf_buffer, headers=headers, media_type='application/pdf')
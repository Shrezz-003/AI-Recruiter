from fastapi import APIRouter, Depends
from app.schemas.job import ResumeInput
from app.services import ai_recruiter_service # <-- Import the new service
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.post("/fitness-check")
def fitness_check(data: ResumeInput, current_user: User = Depends(deps.get_current_user)):
    # Call the new, fully AI-integrated service
    analysis = ai_recruiter_service.get_ai_match_analysis(
        job_description=data.job_description,
        resume_text=data.resume_text
    )
    return analysis
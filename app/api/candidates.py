from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import text_extractor, resume_parser

router = APIRouter()


@router.post("/candidates/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a .pdf or .docx file."
        )

    # 1. Extract raw text from the file
    raw_text = text_extractor.extract_text(file)
    if not raw_text:
        raise HTTPException(status_code=500, detail="Could not extract text from file.")

    # 2. Parse the raw text to find skills
    skills = resume_parser.extract_skills(raw_text)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "extracted_skills": skills
    }
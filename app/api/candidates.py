# File: app/api/candidates.py
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

@router.post("/candidates/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .pdf or .docx file.")

    # In the next step, we will add the text extraction logic here.
    # For now, let's just return the filename.
    return {"filename": file.filename, "content_type": file.content_type}
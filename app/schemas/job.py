from pydantic import BaseModel

class JobDescription(BaseModel):
    title: str
    description: str

class ResumeInput(BaseModel):
    job_description: str
    resume_text: str
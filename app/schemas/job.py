# File: app/schemas/job.py
from pydantic import BaseModel

class JobDescription(BaseModel):
    title: str
    description: str
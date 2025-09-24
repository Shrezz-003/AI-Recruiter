from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

from app.api import auth, employee, employer

app = FastAPI(title="AI Recruitment Assistant API")

# Include all the new routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(employee.router, prefix="/employee", tags=["Employee Tools"])
app.include_router(employer.router, prefix="/employer", tags=["Employer Tools"])

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "API is running!"}
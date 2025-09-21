# File: app/main.py
from fastapi import FastAPI
from app.api import jobs # Import the new jobs router
from dotenv import load_dotenv
from fastapi import FastAPI
from app.api import candidates # Import the candidates router

load_dotenv() 

app = FastAPI(title="AI Recruitment Assistant API")
@app.get("/")
def read_root():
    return {"status": "API is running!"}

app = FastAPI(title="AI Recruitment Assistant API")

app.include_router(candidates.router, tags=["Candidates"]) # Include the router

app.include_router(jobs.router, tags=["Jobs"]) # Add the new router

@app.get("/")
def read_root():
    return {"status": "API is running!"}
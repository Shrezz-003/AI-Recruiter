# File: app/main.py
from fastapi import FastAPI

app = FastAPI(title="AI Recruitment Assistant API")

@app.get("/")
def read_root():
    return {"status": "API is running!"}

# File: app/main.py
from fastapi import FastAPI
from app.api import candidates # Import the candidates router

app = FastAPI(title="AI Recruitment Assistant API")

app.include_router(candidates.router, tags=["Candidates"]) # Include the router

@app.get("/")
def read_root():
    return {"status": "API is running!"}
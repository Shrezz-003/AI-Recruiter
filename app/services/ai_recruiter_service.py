import os
import google.generativeai as genai
import json
from app.core.config import settings

# Configure the Gemini API client
if settings.GOOGLE_API_KEY:
    genai.configure(api_key=settings.GOOGLE_API_KEY)


def get_gemini_model():
    if settings.GOOGLE_API_KEY:
        # Use the requested Gemini 1.5 Flash model
        return genai.GenerativeModel('gemini-1.5-flash-latest')
    return None


def get_ai_match_analysis(job_description: str, resume_text: str):
    """
    Uses Google Gemini to provide a deep, intelligent analysis of a resume.
    """
    model = get_gemini_model()
    if not model:
        return {"error": "AI model not configured. Please set the GOOGLE_API_KEY."}

    prompt = f"""
    As an expert technical recruiter, analyze the resume against the job description and provide a structured JSON evaluation.

    **Job Description:**
    ---
    {job_description}
    ---

    **Resume Text:**
    ---
    {resume_text}
    ---

    **Instructions:**
    1.  **Fit Score:** A percentage score (0-100) of the candidate's fit.
    2.  **Skills Analysis:** List key job skills and if the candidate possesses them ("Yes", "No", "Partial").
    3.  **Strengths:** 2-3 bullet points on strengths for this role.
    4.  **Weaknesses:** 2-3 bullet points on gaps for this role.
    5.  **Verdict:** A one-sentence recommendation.

    **Return a single, valid JSON object only.**

    **JSON Schema:**
    {{
      "fit_score_percent": <integer>,
      "skills_analysis": [{{ "skill": "<skill_name>", "possessed": "<Yes/No/Partial>" }}],
      "strengths": ["<bullet_point>"],
      "weaknesses": ["<bullet_point>"],
      "verdict": "<recommendation>"
    }}
    """
    try:
        # --- THIS IS THE INCORPORATED CHANGE ---
        response = model.generate_content(
            prompt,
            request_options={"timeout": 20}
        )
        # ------------------------------------

        json_response = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(json_response)
    except Exception as e:
        print(f"An error occurred during AI analysis: {e}")
        # Re-raise the exception to see the full traceback in the terminal
        raise e
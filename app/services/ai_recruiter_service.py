import os
import json
import google.generativeai as genai
from app.core.config import settings

# Configure Gemini API
if settings.GOOGLE_API_KEY:
    genai.configure(api_key=settings.GOOGLE_API_KEY)

def get_gemini_model():
    if settings.GOOGLE_API_KEY:
        return genai.GenerativeModel('gemini-1.5-flash-latest')
    return None

def get_ai_match_analysis(job_description: str, resume_text: str):
    model = get_gemini_model()
    if not model:
        return {"error": "AI model not configured. Please set the GOOGLE_API_KEY."}

    prompt = f"""
As an expert technical recruiter, analyze the resume against the job description and provide a structured JSON evaluation.

Job Description:
---
{job_description}
---

Resume Text:
---
{resume_text}
---

Instructions:
1. Fit Score: A percentage score (0-100) of the candidate's fit.
2. Skills Analysis: List key job skills and if the candidate possesses them ("Yes", "No", "Partial").
3. Strengths: 2-3 bullet points on strengths for this role.
4. Weaknesses: 2-3 bullet points on gaps for this role.
5. Verdict: A one-sentence recommendation.

Return a single, valid JSON object only.

JSON Schema:
{{
  "fit_score_percent": <integer>,
  "skills_analysis": [{{ "skill": "<skill_name>", "possessed": "<Yes/No/Partial>" }}],
  "strengths": ["<bullet_point>"],
  "weaknesses": ["<bullet_point>"],
  "verdict": "<recommendation>"
}}
"""

    try:
        response = model.generate_content(prompt)

        # --- Debug raw response ---
        print("\n--- RAW GEMINI RESPONSE ---")
        print(response.text)
        print("--- END OF RAW RESPONSE ---\n")

        # Clean and parse response
        cleaned = response.text.strip().replace('```json', '').replace('```', '')

        if not cleaned:
            return {"error": "Empty response from AI model."}

        try:
            parsed_json = json.loads(cleaned)
            return parsed_json
        except json.JSONDecodeError as json_err:
            print("JSON parsing failed:", json_err)
            print("Raw cleaned response:\n", cleaned)
            return {"error": "Invalid JSON received from AI model."}

    except Exception as e:
        print("\n--- DEBUG: A DETAILED ERROR OCCURRED IN THE AI SERVICE ---")
        print(f"The specific error is: {e}")
        print("--- END OF DEBUG ---\n")
        return {"error": "Failed to get a valid analysis from the AI model."}

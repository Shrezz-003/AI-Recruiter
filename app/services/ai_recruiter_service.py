import os
import google.generativeai as genai
import json
from app.core.config import settings

# Configure the Gemini API client
if settings.GOOGLE_API_KEY:
    genai.configure(api_key=settings.GOOGLE_API_KEY)
else:
    print("WARNING: GOOGLE_API_KEY not found. AI Recruiter Service will be disabled.")

def get_gemini_model():
    if settings.GOOGLE_API_KEY:
        return genai.GenerativeModel('gemini-pro')
    return None

def get_ai_match_analysis(job_description: str, resume_text: str):
    """
    Uses an LLM to provide a deep, intelligent analysis of a resume against a job description.
    """
    model = get_gemini_model()
    if not model:
        return {"error": "AI model not configured. Please set the GOOGLE_API_KEY."}

    # This is a highly engineered prompt for professional-level results
    prompt = f"""
    As an expert technical recruiter with 20 years of experience, your task is to analyze the following resume and job description. Provide a comprehensive evaluation in a structured JSON format.

    **Job Description:**
    ---
    {job_description}
    ---

    **Resume Text:**
    ---
    {resume_text}
    ---

    **Instructions:**
    1.  **Overall Fit Score:** Provide a percentage score from 0 to 100 representing how well this candidate fits the role. Consider experience, skills, and overall profile.
    2.  **Skills Analysis:** Identify the key skills required by the job. For each required skill, indicate if the candidate possesses it ("Yes", "No", or "Partial").
    3.  **Strengths:** Provide a brief, 2-3 bullet point summary of the candidate's key strengths as they relate to this specific job.
    4.  **Areas for Improvement:** Provide a 2-3 bullet point summary of potential gaps or areas where the candidate could be stronger for this role.
    5.  **Final Verdict:** Give a concise, one-sentence recommendation (e.g., "Strongly Recommend Interview", "Recommend Interview", "Consider with Reservations", "Not a good fit").

    **Return your response as a single, valid JSON object only. Do not include any other text or formatting.**

    **JSON Schema to follow:**
    {{
      "fit_score_percent": <integer>,
      "skills_analysis": [
        {{
          "skill": "<skill_name>",
          "possessed": "<Yes/No/Partial>"
        }}
      ],
      "strengths": [
        "<bullet_point_summary>"
      ],
      "weaknesses": [
        "<bullet_point_summary>"
      ],
      "verdict": "<one_sentence_recommendation>"
    }}
    """

    try:
        response = model.generate_content(prompt)
        # Clean up the response to ensure it's valid JSON
        json_response = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(json_response)
    except Exception as e:
        print(f"An error occurred during AI analysis: {e}")
        return {"error": "Failed to get a valid analysis from the AI model."}
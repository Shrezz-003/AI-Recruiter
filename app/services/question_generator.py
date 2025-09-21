import os
import google.generativeai as genai
import json

# Get the API key from the environment variables loaded at startup
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Configure the Gemini API client only if the key exists
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    # Handle the case where the API key is not set
    model = None
    print("WARNING: GOOGLE_API_KEY environment variable not found. Question generation will be disabled.")


def generate_interview_questions(skills: list[str]):
    # Check if the model was initialized successfully
    if not model:
        return {"error": "API key not configured. Cannot generate questions."}

    prompt = f"""
    You are an expert technical interviewer. Generate 3 interview questions to assess a candidate's proficiency in the following skills: {', '.join(skills)}.
    
    For each question, provide:
    1. A "question" text.
    2. A "category" (e.g., "Technical Knowledge", "Problem Solving", "Behavioral").
    3. A "difficulty" (e.g., "Easy", "Medium", "Hard").
    
    Return the output as a valid JSON object in the following format:
    {{
      "questions": [
        {{
          "question": "Your generated question here.",
          "category": "The category of the question.",
          "difficulty": "The difficulty of the question."
        }}
      ]
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean up the response to extract the JSON part
        json_response = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(json_response)
    except Exception as e:
        print(f"An error occurred during question generation: {e}")
        return {"error": "Failed to generate or parse questions from the LLM."}
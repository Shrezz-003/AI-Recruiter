# File: app/services/matching_service.py
from sentence_transformers import SentenceTransformer, util

# Load a pre-trained model. This will be downloaded on the first run.
# 'all-MiniLM-L6-v2' is a great, lightweight model for this task.
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_fit_score(resume_skills: list[str], jd_skills: list[str]):
    if not resume_skills or not jd_skills:
        return 0.0

    # Generate embeddings for both lists of skills
    resume_embeddings = model.encode(resume_skills, convert_to_tensor=True)
    jd_embeddings = model.encode(jd_skills, convert_to_tensor=True)

    # Calculate cosine similarity between the embeddings
    # This gives a score indicating how similar the skill sets are in meaning
    cosine_scores = util.cos_sim(resume_embeddings, jd_embeddings)

    # We can use the average of the highest score for each resume skill
    # as our final "fit score".
    # For each resume skill, find the highest similarity score against all JD skills.
    top_scores = [max(scores) for scores in cosine_scores]
    average_score = sum(top_scores) / len(top_scores)

    # Convert to a percentage
    return round(float(average_score) * 100, 2)
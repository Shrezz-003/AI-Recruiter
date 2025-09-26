from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_fit_score(resume_skills: list[str], jd_skills: list[str]):
    if not resume_skills or not jd_skills:
        return 0.0

    resume_embeddings = model.encode(resume_skills, convert_to_tensor=True)
    jd_embeddings = model.encode(jd_skills, convert_to_tensor=True)

    cosine_scores = util.cos_sim(resume_embeddings, jd_embeddings)

    # Average max similarity for each resume skill
    top_scores_per_resume_skill = torch.max(cosine_scores, dim=1).values
    resume_to_jd_score = torch.mean(top_scores_per_resume_skill).item()

    # Average max similarity for each JD skill
    top_scores_per_jd_skill = torch.max(cosine_scores, dim=0).values
    jd_coverage_score = torch.mean(top_scores_per_jd_skill).item()

    # Combined score
    combined_score = (resume_to_jd_score + jd_coverage_score) / 2

    return round(combined_score * 100, 2)

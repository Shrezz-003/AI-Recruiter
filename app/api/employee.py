from fastapi import APIRouter, Depends
from app.schemas.job import ResumeInput
from app.services import resume_parser, question_generator, matching_service

router = APIRouter()


@router.post("/fitness-check")
def fitness_check(data: ResumeInput):
    resume_skills = resume_parser.extract_skills(data.resume_text)
    jd_skills = resume_parser.extract_skills(data.job_description)

    score = matching_service.calculate_fit_score(resume_skills, jd_skills)

    # Logic to determine skills user has vs. doesn't have
    user_has_skills = list(set(resume_skills) & set(jd_skills))
    user_lacks_skills = list(set(jd_skills) - set(resume_skills))

    return {
        "fit_score_percent": score,
        "required_skills": jd_skills,
        "candidate_has_skills": user_has_skills,
        "candidate_lacks_skills": user_lacks_skills
    }


@router.post("/expected-questions")
def get_expected_questions(data: ResumeInput):
    # Generate questions based on skills the user lacks but are required for the job
    skills_for_questions = list(set(resume_parser.extract_skills(data.job_description)))

    if not skills_for_questions:
        return {"message": "No relevant skills found to generate questions."}

    questions = question_generator.generate_interview_questions(skills_for_questions)
    return questions
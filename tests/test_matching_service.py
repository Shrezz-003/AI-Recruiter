from app.services.matching_service import calculate_fit_score

def test_calculate_fit_score():
    # Scenario 1: Perfect match
    resume_skills_1 = ["python", "fastapi", "docker"]
    jd_skills_1 = ["python", "fastapi", "docker"]
    score_1 = calculate_fit_score(resume_skills_1, jd_skills_1)
    print(f"\nScenario 1 (Perfect Match) Score: {score_1}")
    assert 95.0 < score_1 <= 100.0

    # Scenario 2: Partial match
    resume_skills_2 = ["python", "fastapi"]
    jd_skills_2 = ["python", "fastapi", "docker", "aws"]
    score_2 = calculate_fit_score(resume_skills_2, jd_skills_2)
    print(f"Scenario 2 (Partial Match) Score: {score_2}")
    assert 50.0 < score_2 < 95.0

    # Scenario 3: No match
    resume_skills_3 = ["java", "spring"]
    jd_skills_3 = ["python", "fastapi"]
    score_3 = calculate_fit_score(resume_skills_3, jd_skills_3)
    print(f"Scenario 3 (No Match) Score: {score_3}")
    assert score_3 < 50.0

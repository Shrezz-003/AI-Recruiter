import spacy
from spacy.matcher import Matcher
import json
import os


# --- MODIFIED PART ---
def load_skills_from_json(file_path):
    """Loads a flattened list of skills from a categorized JSON file."""
    if not os.path.exists(file_path):
        # Handle case where file might be missing in production
        return []

    with open(file_path, 'r') as f:
        skills_data = json.load(f)

    # Flatten the list of skills from all categories into a single list
    all_skills = []
    for category in skills_data:
        all_skills.extend(skills_data[category])

    return all_skills


# Construct the absolute path to the skills JSON file
# This is more reliable than a relative path
SKILLS_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'skills_db.json')
SKILLS_DB = load_skills_from_json(SKILLS_FILE_PATH)
# --- END OF MODIFIED PART ---


# Load the spaCy model once when the module is loaded
nlp = spacy.load("en_core_web_sm")


def extract_skills(resume_text: str):
    """Extracts skills from resume text using a predefined skill list."""

    matcher = Matcher(nlp.vocab)

    for skill in SKILLS_DB:
        pattern = [{"LOWER": word} for word in skill.lower().split()]
        matcher.add(skill, [pattern])

    doc = nlp(resume_text.lower())  # Process text in lowercase for better matching
    matches = matcher(doc)

    found_skills = set()
    for match_id_as_int, start, end in matches:
        skill_string = nlp.vocab.strings[match_id_as_int]
        found_skills.add(skill_string)

    return list(found_skills)
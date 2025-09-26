import spacy
from spacy.matcher import Matcher
import re
import json
import os

nlp = spacy.load("en_core_web_lg")


def load_skills_from_json(file_path):
    # ... (this function remains the same)
    if not os.path.exists(file_path): return []
    with open(file_path, 'r', encoding='utf-8') as f: skills_data = json.load(f)
    all_skills = [skill for category in skills_data for skill in skills_data[category]]
    return all_skills


SKILLS_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'skills_db.json')
SKILLS_DB = load_skills_from_json(SKILLS_FILE_PATH)


def extract_contact_info(text):
    email = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    phone = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', text)
    return email.group(0) if email else None, phone.group(0) if phone else None


def extract_name(doc):
    for ent in doc.ents:
        if ent.label_ == 'PERSON' and len(ent.text.split()) > 1:
            return ent.text
    return None


def extract_skills(doc):
    matcher = Matcher(nlp.vocab)
    for skill in SKILLS_DB:
        pattern = [{"LOWER": word} for word in skill.lower().split()]
        matcher.add(skill, [pattern])

    matches = matcher(doc)
    return list(set(nlp.vocab.strings[match_id] for match_id, start, end in matches))


def professional_resume_parser(text: str):
    doc = nlp(text)
    name = extract_name(doc)
    email, phone = extract_contact_info(text)
    skills = extract_skills(doc)

    return {
        "contact_info": {"name": name, "email": email, "phone": phone},
        "skills": skills
    }
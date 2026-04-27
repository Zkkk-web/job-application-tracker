"""
resume.py — Resume builder logic for ApplyTrack
Place in: src/resume.py
"""

import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data.json')
USERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'users.json')


def _load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def _load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)


def _save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)


def get_resume_profile(username: str) -> dict:
    """
    Returns the user's saved resume profile (personal info, skills, education, etc.)
    Falls back to empty defaults if not yet set.
    """
    users = _load_users()
    user = users.get(username, {})
    return user.get("resume_profile", {
        "full_name": username,
        "email": "",
        "phone": "",
        "location": "",
        "linkedin": "",
        "github": "",
        "summary": "",
        "skills": [],
        "education": [],
    })


def save_resume_profile(username: str, profile: dict) -> bool:
    """
    Saves the user's resume profile to users.json.
    Returns True on success.
    """
    users = _load_users()
    if username not in users:
        users[username] = {}
    users[username]["resume_profile"] = profile
    _save_users(users)
    return True


def generate_resume_data(username: str) -> dict:
    """
    Generates a full resume data structure by combining:
    - The user's saved resume profile (personal info, skills, education)
    - Their application history (companies applied to, offers received)

    Returns a complete dict ready to be rendered by resume.html
    """
    profile = get_resume_profile(username)
    data = _load_data()
    apps = data.get(username, {}).get("applications", [])

    # Extract experience entries from successful/completed applications
    experience = []
    for app in apps:
        if app.get("status") in ("Offer", "Interview"):
            experience.append({
                "company": app.get("company", ""),
                "role": app.get("role", ""),
                "status": app.get("status"),
                "date_applied": app.get("date_applied", ""),
                "notes": app.get("notes", ""),
            })

    # Application summary stats for the resume header
    total = len(apps)
    offers = sum(1 for a in apps if a.get("status") == "Offer")
    interviews = sum(1 for a in apps if a.get("status") == "Interview")

    return {
        "profile": profile,
        "experience": experience,
        "stats": {
            "total_applications": total,
            "offers": offers,
            "interviews": interviews,
        },
        "generated_at": datetime.now().strftime("%B %d, %Y"),
    }


def get_resume_tips(role: str = "", skills: list = None) -> list:
    """
    Returns a list of context-aware resume writing tips.
    Simple rule-based Python logic — no AI needed.
    """
    tips = [
        "Use strong action verbs: 'Built', 'Designed', 'Led', 'Automated', 'Improved'.",
        "Quantify achievements where possible: 'Reduced load time by 40%'.",
        "Tailor your summary to each job description.",
        "Keep your resume to one page unless you have 5+ years of experience.",
        "List skills that appear in the job posting first.",
    ]

    if skills:
        if "Python" in skills or "Flask" in skills:
            tips.append("Highlight backend projects with Python/Flask — show GitHub links.")
        if "SQL" in skills or "SQLite" in skills:
            tips.append("Mention database design decisions, not just 'used SQL'.")

    if role:
        role_lower = role.lower()
        if "data" in role_lower:
            tips.append("For data roles, showcase any analysis or visualization work.")
        elif "frontend" in role_lower or "ui" in role_lower:
            tips.append("For frontend roles, link to a portfolio or live demo.")
        elif "backend" in role_lower or "software" in role_lower:
            tips.append("For backend roles, describe system design and scalability thinking.")

    return tips

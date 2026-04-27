"""
email_utils.py — Email draft generation for ApplyTrack
Place in: src/email_utils.py
"""

import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data.json')

# All supported email draft types
EMAIL_TYPES = [
    "follow_up",
    "thank_you",
    "withdraw",
    "accept_offer",
    "decline_offer",
    "request_feedback",
]

EMAIL_TYPE_LABELS = {
    "follow_up":        "Follow-Up After Applying",
    "thank_you":        "Thank You After Interview",
    "withdraw":         "Withdraw Application",
    "accept_offer":     "Accept Job Offer",
    "decline_offer":    "Decline Job Offer",
    "request_feedback": "Request Feedback After Rejection",
}


def _load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def get_application(username: str, app_id: str) -> dict | None:
    """Fetches a single application by ID."""
    data = _load_data()
    apps = data.get(username, {}).get("applications", [])
    for app in apps:
        if str(app.get("id")) == str(app_id):
            return app
    return None


def generate_email_draft(username: str, app_id: str, email_type: str) -> dict:
    """
    Generates an email draft for a specific application and email type.

    Returns:
        {
            "success": True,
            "subject": "...",
            "body": "...",
            "label": "...",
        }
    or
        {"success": False, "error": "..."}
    """
    if email_type not in EMAIL_TYPES:
        return {"success": False, "error": f"Unknown email type: {email_type}"}

    app = get_application(username, app_id)
    if not app:
        return {"success": False, "error": "Application not found"}

    company = app.get("company", "the company")
    role = app.get("role", "the position")
    date_applied = app.get("date_applied", "recently")
    interviewer = app.get("interviewer_name", "Hiring Manager")

    templates = {
        "follow_up": {
            "subject": f"Following Up – {role} Application",
            "body": (
                f"Dear {interviewer},\n\n"
                f"I hope this message finds you well. I wanted to follow up on my application "
                f"for the {role} position at {company}, submitted on {date_applied}.\n\n"
                f"I remain very enthusiastic about this opportunity and would love to discuss "
                f"how my background aligns with the team's needs. Please let me know if there "
                f"is any additional information I can provide.\n\n"
                f"Thank you for your time and consideration.\n\n"
                f"Best regards,\n{username}"
            )
        },
        "thank_you": {
            "subject": f"Thank You – {role} Interview",
            "body": (
                f"Dear {interviewer},\n\n"
                f"Thank you so much for taking the time to speak with me about the {role} role "
                f"at {company}. I really enjoyed our conversation and learning more about the team's work.\n\n"
                f"Our discussion reinforced my excitement about this opportunity. I'm confident "
                f"that my skills in [mention relevant skill] would be a great fit for your team's goals.\n\n"
                f"Please don't hesitate to reach out if you need any further information. I look "
                f"forward to hearing from you.\n\n"
                f"Warm regards,\n{username}"
            )
        },
        "withdraw": {
            "subject": f"Withdrawing Application – {role}",
            "body": (
                f"Dear {interviewer},\n\n"
                f"I am writing to formally withdraw my application for the {role} position at {company}.\n\n"
                f"After careful consideration, I have decided to pursue a different opportunity "
                f"that is a better fit for my current goals. I truly appreciate the time and "
                f"effort your team invested in reviewing my application.\n\n"
                f"I hold {company} in high regard and hope our paths may cross again in the future.\n\n"
                f"Thank you again for your understanding.\n\n"
                f"Best regards,\n{username}"
            )
        },
        "accept_offer": {
            "subject": f"Offer Acceptance – {role} at {company}",
            "body": (
                f"Dear {interviewer},\n\n"
                f"I am thrilled to formally accept the offer for the {role} position at {company}. "
                f"Thank you so much for this opportunity — I'm genuinely excited to join the team.\n\n"
                f"Please let me know the next steps regarding onboarding paperwork or any "
                f"information I should prepare ahead of my start date.\n\n"
                f"Looking forward to working together!\n\n"
                f"Best regards,\n{username}"
            )
        },
        "decline_offer": {
            "subject": f"Offer Decision – {role} at {company}",
            "body": (
                f"Dear {interviewer},\n\n"
                f"Thank you so much for offering me the {role} position at {company}. After "
                f"thoughtful consideration, I have decided to respectfully decline the offer.\n\n"
                f"This was not an easy decision — I have a great deal of respect for {company} "
                f"and the team. However, I have chosen to accept a role that more closely aligns "
                f"with my current career direction.\n\n"
                f"I hope we have the opportunity to work together in the future. Thank you again "
                f"for your time and generosity throughout this process.\n\n"
                f"Warmly,\n{username}"
            )
        },
        "request_feedback": {
            "subject": f"Feedback Request – {role} Application",
            "body": (
                f"Dear {interviewer},\n\n"
                f"Thank you for letting me know about your decision regarding the {role} role "
                f"at {company}. While I'm disappointed, I truly appreciate the opportunity to "
                f"have been considered.\n\n"
                f"If you have a moment, I would be very grateful for any feedback you could "
                f"share about my application or interview performance. I am always looking to "
                f"grow and improve, and your insights would be incredibly valuable.\n\n"
                f"Thank you for your time.\n\n"
                f"Best regards,\n{username}"
            )
        },
    }

    draft = templates[email_type]
    return {
        "success": True,
        "subject": draft["subject"],
        "body": draft["body"],
        "label": EMAIL_TYPE_LABELS[email_type],
        "company": company,
        "role": role,
    }


def get_all_email_types() -> list:
    """Returns list of all email type dicts for the dropdown menu."""
    return [
        {"type": t, "label": EMAIL_TYPE_LABELS[t]}
        for t in EMAIL_TYPES
    ]

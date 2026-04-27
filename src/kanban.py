"""
kanban.py — Kanban board logic for ApplyTrack
Place in: src/kanban.py
"""

import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data.json')

# The valid status pipeline — order matters for display
STATUS_PIPELINE = [
    "Pending",
    "Applied",
    "Written Test",
    "Interview",
    "Offer",
    "Rejected"
]

# Which transitions are allowed (from -> list of valid next statuses)
ALLOWED_TRANSITIONS = {
    "Pending":    ["Applied", "Rejected"],
    "Applied":     ["Written Test", "Interview", "Rejected"],
    "Written Test": ["Interview", "Rejected"],
    "Interview":   ["Offer", "Rejected"],
    "Offer":       [],
    "Rejected":    [],
}


def _load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def _save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_board(username: str) -> dict:
    """
    Returns applications grouped by status column for the kanban board.

    Returns:
        {
            "Pending": [...],
            "Applied": [...],
            "Written Test": [...],
            "Interview": [...],
            "Offer": [...],
            "Rejected": [...]
        }
    """
    data = _load_data()
    apps = data.get(username, {}).get("applications", [])

    board = {status: [] for status in STATUS_PIPELINE}
    for app in apps:
        status = app.get("status", "Pending")
        if status in board:
            board[status].append(app)

    return board


def move_card(username: str, app_id: str, new_status: str) -> dict:
    """
    Moves an application card to a new status column.
    Validates the transition is allowed.

    Returns:
        {"success": True, "app": {...}} on success
        {"success": False, "error": "..."} on failure
    """
    if new_status not in STATUS_PIPELINE:
        return {"success": False, "error": f"Invalid status: {new_status}"}

    data = _load_data()
    apps = data.get(username, {}).get("applications", [])

    for app in apps:
        if str(app.get("id")) == str(app_id):
            current_status = app.get("status", "Pending")
            allowed = ALLOWED_TRANSITIONS.get(current_status, [])

            if new_status not in allowed:
                return {
                    "success": False,
                    "error": f"Cannot move from '{current_status}' to '{new_status}'"
                }

            app["status"] = new_status
            app["last_updated"] = datetime.now().strftime("%Y-%m-%d")

            # Log status history
            if "history" not in app:
                app["history"] = []
            app["history"].append({
                "from": current_status,
                "to": new_status,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

            _save_data(data)
            return {"success": True, "app": app}

    return {"success": False, "error": "Application not found"}


def get_pipeline_stats(username: str) -> dict:
    """
    Returns count of applications per status column.
    Used for the stats bar above the kanban board.
    """
    board = get_board(username)
    return {status: len(cards) for status, cards in board.items()}


def get_allowed_transitions(current_status: str) -> list:
    """Returns the list of valid next statuses from a given status."""
    return ALLOWED_TRANSITIONS.get(current_status, [])

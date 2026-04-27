"""
calendar_utils.py — Calendar view logic for ApplyTrack
Place in: src/calendar_utils.py
"""

import json
import os
import calendar
from datetime import datetime, date

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data.json')

# Status colors for calendar event dots
STATUS_COLORS = {
        "Pending": "#c8f1f4",
        "Applied": "#D3E8C7",
        "Written Test": "#f7e0d9",
        "Interview": "#d4b7e0",
        "Offer": "#2c9156",
        "Rejected": "#e7a69f"
    }

def _load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def get_month_events(username: str, year: int, month: int) -> dict:
    """
    Returns all application events for a given month, keyed by day number.

    Returns:
        {
            day_number: [
                {
                    "id": "...",
                    "company": "...",
                    "role": "...",
                    "status": "...",
                    "color": "#...",
                    "event_type": "applied" | "interview" | "deadline"
                },
                ...
            ]
        }
    """
    data = _load_data()
    apps = data.get(username, {}).get("applications", [])
    events = {}

    for app in apps:
        # Check application date
        for date_field, event_label in [
            ("date_pending", "pending"),
            ("date_applied", "applied"),
            ("date_written_test", "written_test"),
            ("interview_date", "interview"),
            ("date_offer", "offer"),
            ("deadline", "deadline"),
        ]:
            raw_date = app.get(date_field)
            if not raw_date:
                continue

            try:
                parsed = datetime.strptime(raw_date[:10], "%Y-%m-%d").date()
            except ValueError:
                continue

            if parsed.year == year and parsed.month == month:
                day = parsed.day
                if day not in events:
                    events[day] = []
                events[day].append({
                    "id": app.get("id"),
                    "company": app.get("company", "Unknown"),
                    "role": app.get("role", ""),
                    "status": app.get("status", "Applied"),
                    "color": STATUS_COLORS.get(app.get("status", "Applied"), "#6c757d"),
                    "event_type": event_label,
                })

    return events


def get_calendar_grid(year: int, month: int) -> dict:
    """
    Returns all metadata needed to render a monthly calendar grid.

    Returns:
        {
            "year": int,
            "month": int,
            "month_name": str,
            "weeks": [[day_num or None, ...], ...],  # None = empty cell
            "today": int or None,
            "prev_month": {"year": int, "month": int},
            "next_month": {"year": int, "month": int},
        }
    """
    cal = calendar.monthcalendar(year, month)
    today = date.today()
    today_day = today.day if (today.year == year and today.month == month) else None

    # Previous month
    if month == 1:
        prev = {"year": year - 1, "month": 12}
    else:
        prev = {"year": year, "month": month - 1}

    # Next month
    if month == 12:
        next_ = {"year": year + 1, "month": 1}
    else:
        next_ = {"year": year, "month": month + 1}

    return {
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month],
        "weeks": cal,          # list of weeks; each week is [Mon..Sun], 0 = empty
        "today": today_day,
        "prev_month": prev,
        "next_month": next_,
    }


def get_upcoming_events(username: str, limit: int = 5) -> list:
    """
    Returns the next N upcoming interview/deadline events from today.
    Used for the sidebar or dashboard widget.
    """
    data = _load_data()
    apps = data.get(username, {}).get("applications", [])
    today = date.today()
    upcoming = []

    for app in apps:
        for date_field, label in [("interview_date", "Interview"), ("deadline", "Deadline")]:
            raw = app.get(date_field)
            if not raw:
                continue
            try:
                parsed = datetime.strptime(raw[:10], "%Y-%m-%d").date()
            except ValueError:
                continue
            if parsed >= today:
                upcoming.append({
                    "company": app.get("company", "Unknown"),
                    "role": app.get("role", ""),
                    "date": parsed.strftime("%b %d, %Y"),
                    "type": label,
                    "days_away": (parsed - today).days,
                    "color": STATUS_COLORS.get(app.get("status", "Applied"), "#6c757d"),
                })

    upcoming.sort(key=lambda x: x["days_away"])
    return upcoming[:limit]

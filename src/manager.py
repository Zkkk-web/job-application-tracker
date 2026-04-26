import json
import os

DATA_FILE = "data.json"

def load_applications(user):
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        all_data = json.load(f)
    return all_data.get(user, [])

def save_applications(user, applications):
    all_data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            all_data = json.load(f)
    all_data[user] = applications
    with open(DATA_FILE, "w") as f:
        json.dump(all_data, f, indent=4)

def add_application(user, new_app):
    applications = load_applications(user)
    applications.append(new_app)
    save_applications(user, applications)

def delete_application(user, index):
    applications = load_applications(user)
    if 0 <= index < len(applications):
        applications.pop(index)
        save_applications(user, applications)

def update_status(user, index, new_status):
    applications = load_applications(user)
    if 0 <= index < len(applications):
        applications[index]["status"] = new_status
        save_applications(user, applications)
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

def add_application(user):
    applications = load_applications(user)
    print("\n--- Add Application ---")
    company = input("Company name: ")
    position = input("Position: ")
    date = input("Application date (YYYY-MM-DD): ")
    status = "Pending"
    application = {
        "company": company,
        "position": position,
        "date": date,
        "status": status
    }
    applications.append(application)
    save_applications(user, applications)
    print("Application added successfully!")

def delete_application(user):
    applications = load_applications(user)
    if not applications:
        print("No applications found!")
        return
    print("\n--- Delete Application ---")
    for i, app in enumerate(applications):
        print(f"{i+1}. {app['company']} - {app['position']} ({app['status']})")
    try:
        choice = int(input("Select number to delete: ")) - 1
        if 0 <= choice < len(applications):
            removed = applications.pop(choice)
            save_applications(user, applications)
            print(f"Deleted: {removed['company']} - {removed['position']}")
        else:
            print("Invalid selection!")
    except ValueError:
        print("Please enter a valid number!")

def update_status(user):
    applications = load_applications(user)
    if not applications:
        print("No applications found!")
        return
    print("\n--- Update Status ---")
    for i, app in enumerate(applications):
        print(f"{i+1}. {app['company']} - {app['position']} ({app['status']})")
    try:
        choice = int(input("Select number to update: ")) - 1
        if 0 <= choice < len(applications):
            statuses = ["Pending", "Applied", "Written Test", "Interview", "Offer", "Rejected"]
            print("Select new status:")
            for i, s in enumerate(statuses):
                print(f"{i+1}. {s}")
            status_choice = int(input("Select: ")) - 1
            if 0 <= status_choice < len(statuses):
                applications[choice]["status"] = statuses[status_choice]
                save_applications(user, applications)
                print("Status updated successfully!")
        else:
            print("Invalid selection!")
    except ValueError:
        print("Please enter a valid number!")
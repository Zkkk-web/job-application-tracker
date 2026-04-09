import json
import os

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register():
    users = load_users()
    print("\n--- Register ---")
    username = input("Enter username: ")
    if username in users:
        print("Username already exists!")
        return None
    password = input("Enter password: ")
    users[username] = password
    save_users(users)
    print(f"Registration successful! Welcome {username}")
    return username

def login():
    users = load_users()
    print("\n--- Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username in users and users[username] == password:
        print(f"Login successful! Welcome back {username}")
        return username
    else:
        print("Invalid username or password!")
        return None
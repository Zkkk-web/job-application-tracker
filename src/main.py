from src.auth import login, register
from src.menu import main_menu

def main():
    print("=" * 40)
    print("  Job Application Tracker")
    print("=" * 40)
    print("1. Login")
    print("2. Register")
    choice = input("Please select: ")
    
    if choice == "1":
        user = login()
    elif choice == "2":
        user = register()
    else:
        print("Invalid input!")
        return
    
    if user:
        main_menu(user)

if __name__ == "__main__":
    main()
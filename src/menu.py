from manager import add_application, delete_application, update_status, load_applications
from display import show_all, filter_by_status
from stats import show_stats, generate_chart


def main_menu(user):
    while True:
        print("\n" + "=" * 40)
        print(f"  Welcome, {user}!")
        print("=" * 40)
        print("1. View all applications")
        print("2. Add application")
        print("3. Update status")
        print("4. Delete application")
        print("5. Filter by status")
        print("6. View statistics")
        print("7. View chart")
        print("0. Exit")

        choice = input("Please select: ")
        applications = load_applications(user)

        if choice == "1":
            show_all(applications)
        elif choice == "2":
            add_application(user)
        elif choice == "3":
            update_status(user)
        elif choice == "4":
            delete_application(user)
        elif choice == "5":
            filter_by_status(applications)
        elif choice == "6":
            show_stats(applications)
        elif choice == "7":
            generate_chart(applications)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid input!")
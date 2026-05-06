def show_all(applications):
    if not applications:
        print("No applications found!")
        return
    print("\n--- All Applications ---")
    print(f"{'No.':<5} {'Company':<20} {'Position':<20} {'Date':<15} {'Status':<15}")
    print("-" * 75)
    for i, app in enumerate(applications):
        print(f"{i+1:<5} {app['company']:<20} {app['position']:<20} {app['date']:<15} {app['status']:<15}")

def filter_by_status(applications):
    statuses = ["Pending", "Applied", "Written Test", "Interview", "Offer", "Rejected"]
    print("\nSelect status to filter:")
    for i, s in enumerate(statuses):
        print(f"{i+1}. {s}")
    try:
        choice = int(input("Select: ")) - 1
        if 0 <= choice < len(statuses):
            selected = statuses[choice]
            filtered = [app for app in applications if app["status"] == selected]
            if filtered:
                show_all(filtered)
            else:
                print(f"No applications with status: {selected}")
        else:
            print("Invalid selection!")
    except ValueError:
        print("Please enter a valid number!")
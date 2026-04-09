def show_stats(applications):
    if not applications:
        print("No applications found!")
        return
    total = len(applications)
    interviews = sum(1 for app in applications if app["status"] in ["Interview", "Offer"])
    offers = sum(1 for app in applications if app["status"] == "Offer")
    rejected = sum(1 for app in applications if app["status"] == "Rejected")
    interview_rate = (interviews / total * 100) if total > 0 else 0

    print("\n--- Statistics ---")
    print(f"Total Applications : {total}")
    print(f"Interviews         : {interviews}")
    print(f"Offers             : {offers}")
    print(f"Rejected           : {rejected}")
    print(f"Interview Rate     : {interview_rate:.1f}%")

def show_chart(applications):
    try:
        import matplotlib.pyplot as plt
        if not applications:
            print("No applications found!")
            return
        status_counts = {}
        for app in applications:
            status = app["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        plt.figure(figsize=(8, 5))
        plt.bar(status_counts.keys(), status_counts.values(), color="steelblue")
        plt.title("Application Status Overview")
        plt.xlabel("Status")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()
    except ImportError:
        print("matplotlib not installed. Run: pip install matplotlib")
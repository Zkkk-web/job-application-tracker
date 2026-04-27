import json
import os
import matplotlib
matplotlib.use('Agg')  # 不弹出窗口，直接保存图片
import matplotlib.pyplot as plt

def show_stats(applications):
    if not applications:
        return None
    total = len(applications)
    interviews = sum(1 for app in applications if app["status"] in ["Interview", "Offer"])
    offers = sum(1 for app in applications if app["status"] == "Offer")
    rejected = sum(1 for app in applications if app["status"] == "Rejected")
    interview_rate = round(interviews / total * 100, 1) if total > 0 else 0
    return {
        "total": total,
        "interviews": interviews,
        "offers": offers,
        "rejected": rejected,
        "interview_rate": interview_rate
    }

def generate_chart(applications):
    if not applications:
        return False

    status_counts = {}
    for app in applications:
        status = app["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    statuses = list(status_counts.keys())
    counts = list(status_counts.values())
    
    colors = {
        "Pending": "#c8f1f4",
        "Applied": "#D3E8C7",
        "Written Test": "#fccaba",
        "Interview": "#d4b7e0",
        "Offer": "#2c9156",
        "Rejected": "#e7a69f"
    }
    bar_colors = [colors.get(s, "#ced3d6") for s in statuses]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.patch.set_facecolor('#f8f9fa')

    # 饼图
    wedges, texts, autotexts = ax1.pie(
        counts,
        labels=statuses,
        colors=bar_colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops=dict(edgecolor='white', linewidth=2)
    )
    for text in autotexts:
        text.set_fontsize(10)
        text.set_color('black')
        text.set_fontweight('bold')
    ax1.set_title("Status Distribution", fontsize=14, fontweight='bold', pad=15)

    # 柱状图
    bars = ax2.bar(statuses, counts, color=bar_colors,
                   edgecolor='white', linewidth=1.5, width=0.6)
    ax2.set_title("Applications by Status", fontsize=14, fontweight='bold', pad=15)
    ax2.set_xlabel("Status", fontsize=11)
    ax2.set_ylabel("Count", fontsize=11)
    ax2.yaxis.get_major_locator().set_params(integer=True)
    ax2.set_facecolor('#f8f9fa')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.xticks(rotation=15, ha='right')

    # 每个柱子上显示数字
    for bar, count in zip(bars, counts):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                str(count), ha='center', va='bottom', fontweight='bold')

    plt.tight_layout(pad=2)
    chart_path = os.path.join("static", "chart.png")
    plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
    plt.close()
    return True
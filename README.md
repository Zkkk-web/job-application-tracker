好！把 `README.md` 全部替换成这个：

```markdown
# 📋 Job Application Tracker

A full-stack web application built with Python Flask to help students and job seekers track their internship and job applications in one place.

---

## 👥 Team Members
- Member 1: Bacy Zhu
- Member 2: (Partner's name)

---

## ✨ Features

### Core Features
- 🔐 User Registration & Login (SHA-256 password encryption)
- ➕ Add new job applications (company, position, date, status)
- ✏️ Update application status in real-time
- 🗑️ Delete applications
- 📋 View all applications in a clean table layout
- 🔍 Filter applications by status

### Dashboard & Analytics
- 📊 Statistics overview (total applications, interviews, offers, rejection rate)
- 🥧 Pie chart — application status distribution
- 📈 Bar chart — application count by status

### Additional Pages
- 📅 Calendar — track important dates and deadlines
- 🗂️ Kanban Board — visual status tracking (Pending → Applied → Interview → Offer)
- 📄 Resume Builder — build and manage your resume
- ✉️ Email Drafts — save and manage application emails

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Frontend | HTML, CSS, Jinja2 |
| Database | JSON file storage |
| Charts | Matplotlib |
| Auth | SHA-256 encryption (hashlib) |

---

## 🚀 How to Run

### 1. Clone the repository
```
git clone https://github.com/Zkkk-web/job-application-tracker.git
cd job-application-tracker
```

### 2. Install dependencies
```
pip install flask matplotlib
```

### 3. Run the app
```
python app.py
```

### 4. Open in browser
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
job-application-tracker/
├── app.py                  # Flask routes & main application
├── auth.py                 # Login & Register logic
├── manager.py              # Application CRUD operations
├── stats.py                # Statistics & Chart generation
├── display.py              # Display utilities
├── menu.py                 # Terminal menu (CLI version)
├── main.py                 # CLI entry point
├── templates/
│   ├── index.html          # Home / Landing page
│   ├── login.html          # Login page
│   ├── register.html       # Register page
│   ├── dashboard.html      # Main dashboard
│   ├── add.html            # Add new application
│   ├── update.html         # Update application status
│   ├── kanban.html         # Kanban board view
│   ├── resume.html         # Resume builder
│   ├── email_drafts.html   # Email drafts manager
│   └── calendar.html       # Calendar view
├── static/
│   ├── style.css           # Global CSS styles
│   └── chart.png           # Generated statistics chart
├── data.json               # Application data storage
└── users.json              # User credentials storage
```

---

## 📌 Application Status Flow

```
Pending → Applied → Written Test → Interview → Offer ✅
                                             → Rejected ❌
```

---

## 🎯 Purpose

This project was built to solve a real problem for students during job hunting season — keeping track of dozens of applications across different companies and platforms. Instead of using spreadsheets, this app provides a clean, interactive, and visual way to manage the entire job search process.
```

保存完 `git add -A` → `git commit -m "Update README"` → `git push` 😄

# ApplyTrack - Job Application Tracker

## Project Description
A full-stack Python web application that helps students 
track their internship and job applications. Features 
include CRUD operations, status pipeline, statistics 
visualization, Kanban board view, and AI-powered job 
description parsing using the Deepseek API.

## Team Members
- Zhu Kebaichun (Bacy)
- Wong Kei Wai Hadassah

## Installation
1. Clone the repository
   git clone https://github.com/Zkkk-web/job-application-tracker.git

2. Install dependencies
   pip install -r requirements.txt

3. Set up environment variable
   Create a .env file with: DEEPSEEK_API_KEY=your_key_here

## How to Run
python app.py

Then open http://127.0.0.1:5000 in your browser.

## Live Demo
https://job-application-tracker-1wyq.onrender.com

## Dataset
The application uses two JSON files for data storage:
- data.json: Stores all job application records
- users.json: Stores user credentials (passwords hashed with SHA-256)

These files are created automatically on first run.

## Output Explanation
- /dashboard - Main interface showing all applications and statistics
- /kanban - Kanban board view organized by status
- Charts are generated server-side using Matplotlib

## Tech Stack
Python 3, Flask, Matplotlib, Deepseek API, JSON storage, 
HTML/CSS/Jinja2, Gunicorn, Render
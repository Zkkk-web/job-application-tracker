
from flask import Flask, render_template, request, redirect, url_for, session
from auth import register_web, login_web
from manager import load_applications, add_application, save_applications, delete_application, update_status
from stats import show_stats, generate_chart

app = Flask(__name__)
app.secret_key = "job_tracker_secret_key"

# ─── Home ───────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

# ─── Register ───────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success, message = register_web(username, password)
        if success:
            return redirect(url_for('login', success=message))
        else:
            return render_template('register.html', error=message)
    return render_template('register.html')

# ─── Login ──────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success, message = login_web(username, password)
        if success:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error=message)
    success_msg = request.args.get('success')
    return render_template('login.html', success=success_msg)

# ─── Logout ─────────────────────────────────────────
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# ─── Dashboard ──────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    applications = load_applications(username)
    
    stats = show_stats(applications) or {
        'total': 0,
        'interviews': 0,
        'offers': 0,
        'rejected': 0,
        'interview_rate': 0
    }
    
    # 生成图表
    chart_available = generate_chart(applications)
    
    return render_template('dashboard.html',
                           username=username,
                           applications=enumerate(applications),
                           stats=stats,
                           chart_available=chart_available)

# ─── Add Application ────────────────────────────────
@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = session['username']
        new_app = {
            'company': request.form['company'],
            'position': request.form['position'],
            'date': request.form['date'],
            'status': request.form['status']
        }
        add_application(username, new_app)
        return redirect(url_for('dashboard'))
    return render_template('add.html')
# ─── Delete Application ─────────────────────────────
@app.route('/delete/<int:index>')
def delete(index):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    applications = load_applications(username)
    if 0 <= index < len(applications):
        applications.pop(index)
        save_applications(username, applications)
    return redirect(url_for('dashboard'))

# ─── Update Status ──────────────────────────────────
@app.route('/update/<int:index>', methods=['GET', 'POST'])
def update(index):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    applications = load_applications(username)
    if request.method == 'POST':
        applications[index]['status'] = request.form['status']
        save_applications(username, applications)
        return redirect(url_for('dashboard'))
    return render_template('update.html',
                           index=index,
                           app=applications[index])

# ─── Run ────────────────────────────────────────────
@app.route('/board')
def kanban():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    applications = load_applications(username)
    from stats import show_stats
    stats = show_stats(applications) or {
        'total': 0, 'interviews': 0,
        'offers': 0, 'rejected': 0, 'interview_rate': 0
    }
    # 按状态分组
    board = {
        'Pending': [a for a in applications if a['status'] == 'Pending'],
        'Applied': [a for a in applications if a['status'] == 'Applied'],
        'Written Test': [a for a in applications if a['status'] == 'Written Test'],
        'Interview': [a for a in applications if a['status'] == 'Interview'],
        'Offer': [a for a in applications if a['status'] == 'Offer'],
        'Rejected': [a for a in applications if a['status'] == 'Rejected'],
    }
    return render_template('kanban.html', applications=applications, stats=stats, board=board)
@app.route('/calendar')
def calendar_view():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    applications = load_applications(username)
    import calendar
    from datetime import datetime
    now = datetime.now()
    month = int(request.args.get('month', now.month))
    year = int(request.args.get('year', now.year))

    class GridObj:
        pass
    grid = GridObj()
    grid.month_name = f"{calendar.month_name[month]} {year}"
    grid.weeks = calendar.monthcalendar(year, month)
    grid.today = now.day if (month == now.month and year == now.year) else -1
    grid.prev_year = year if month > 1 else year - 1
    grid.prev_month = month - 1 if month > 1 else 12
    grid.next_year = year if month < 12 else year + 1
    grid.next_month = month + 1 if month < 12 else 1

    return render_template('calendar.html',
                           applications=applications,
                           grid=grid,
                           month=month,
                           year=year)
@app.route('/resume', methods=['GET', 'POST'])
def resume():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    applications = load_applications(username)
    from stats import show_stats
    stats = show_stats(applications) or {
        'total': 0, 'interviews': 0,
        'offers': 0, 'rejected': 0, 'interview_rate': 0
    }
    resume_data = {
        'name': '', 'email': '', 'phone': '',
        'linkedin': '', 'github': '', 'location': '',
        'summary': '', 'profile': '', 'education': '',
        'experience': '', 'skills': '',
        'projects': '', 'awards': ''
    }
    return render_template('resume.html',
                           resume=resume_data,
                           username=username,
                           stats=stats,
                           applications=applications)

@app.route('/resume_save', methods=['POST'])
def resume_save():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('resume'))

@app.route('/email-drafts')
def email_drafts():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('email_drafts.html')
if __name__ == '__main__':
    app.run(debug=True)
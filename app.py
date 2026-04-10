
from flask import Flask, render_template, request, redirect, url_for, session
from src.auth import register_web, login_web
from src.manager import load_applications, add_application,save_applications, delete_application, update_status
from src.stats import show_stats, generate_chart

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
        applications = load_applications(username)
        new_app = {
            'company': request.form['company'],
            'position': request.form['position'],
            'date': request.form['date'],
            'status': request.form['status']
        }
        applications.append(new_app)
        from manager import save_applications
        save_applications(username, applications)
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
if __name__ == '__main__':
    app.run(debug=True)
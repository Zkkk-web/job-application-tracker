
import os, json, time as _time
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from src.auth import register_web, login_web
from src.manager import load_applications, add_application, save_applications, delete_application, update_status
from src.stats import show_stats, generate_chart
from jd_parser import parse_jd
# ─── Per-user data helpers ──────────────────────────
DATA_DIR = "data"

def _user_dir(username):
    d = os.path.join(DATA_DIR, username)
    os.makedirs(d, exist_ok=True)
    return d

def load_resumes(username):
    p = os.path.join(_user_dir(username), "resumes.json")
    return json.load(open(p)) if os.path.exists(p) else []

def save_resumes(username, resumes):
    with open(os.path.join(_user_dir(username), "resumes.json"), "w") as f:
        json.dump(resumes, f, indent=2)

def load_cal_events(username):
    p = os.path.join(_user_dir(username), "cal_events.json")
    return json.load(open(p)) if os.path.exists(p) else []

def save_cal_events(username, events):
    with open(os.path.join(_user_dir(username), "cal_events.json"), "w") as f:
        json.dump(events, f, indent=2)

app = Flask(__name__)
app.secret_key = "job_tracker_secret_key"
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.jinja_env.auto_reload = True
app.jinja_env.cache = {}

# ─── Cache Control ──────────────────────────────────
@app.after_request
def disable_cache(response):
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.max_age = 0
    response.cache_control.must_revalidate = True
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

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
            session['username'] = username
            return redirect(url_for('welcome'))
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
            return redirect(url_for('welcome'))
        else:
            return render_template('login.html', error=message)
    success_msg = request.args.get('success')
    return render_template('login.html', success=success_msg)

# ─── Logout ─────────────────────────────────────────
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
# ─── Welcome ───────────────────────────────────────
@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    applications = load_applications(username)
    resumes = load_resumes(username)
    return render_template('welcome.html',
                           username=username,
                           has_applications=len(applications) > 0,
                           has_resume=len(resumes) > 0)

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
# ─── Parse JD ───────────────────────────────────────
@app.route('/parse_jd', methods=['POST'])
def parse_jd_route():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    jd_text = request.form.get('jd_text', '')
    
    try:
        parsed = parse_jd(jd_text)
        return render_template('add.html',
                             prefill=parsed,
                             jd_text=jd_text)
    except Exception as e:
        return render_template('add.html',
                             error=f"Failed to parse JD: {str(e)}")
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
@app.route('/board')
def kanban():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    applications = load_applications(username)
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
    return render_template('kanban.html', applications=applications, stats=stats, board=board, username=username)
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

    cal_events = load_cal_events(username)
    return render_template('calendar.html',
                           applications=applications,
                           cal_events=cal_events,
                           grid=grid,
                           month=month,
                           year=year,
                           username=username)
@app.route('/resume', methods=['GET', 'POST'])
def resume():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    applications = load_applications(username)
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
    username = session['username']
    # Save resume to library via JSON body
    if request.is_json:
        data = request.json or {}
        data['id'] = str(int(_time.time() * 1000))
        resumes = load_resumes(username)
        # Update existing if id matches, else append
        rid = data.get('id')
        idx = next((i for i, r in enumerate(resumes) if str(r.get('id')) == rid), None)
        if idx is not None:
            resumes[idx] = data
        else:
            resumes.append(data)
        save_resumes(username, resumes)
        return jsonify({'ok': True, 'id': data['id']})
    return redirect(url_for('resume'))

@app.route('/email-drafts')
def email_drafts():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    return render_template('email_drafts.html', username=username)


@app.route('/stats')
def stats():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    applications = load_applications(username)
    stats_data = show_stats(applications) or {
        'total': 0, 'interviews': 0,
        'offers': 0, 'rejected': 0, 'interview_rate': 0
    }
    generate_chart(applications)
    
    # 每周投递数据
    from datetime import datetime, timedelta
    weekly = {}
    for app in applications:
        try:
            date = datetime.strptime(app['date'], '%Y-%m-%d')
            week = date.strftime('%Y-W%W')
            weekly[week] = weekly.get(week, 0) + 1
        except:
            pass
    weekly_labels = sorted(weekly.keys())
    weekly_values = [weekly[w] for w in weekly_labels]

    return render_template('stats_page.html',
                           stats=stats_data,
                           applications=applications,
                           weekly_labels=weekly_labels,
                           weekly_values=weekly_values, 
                           username=username)
@app.route('/jobsearch')
def jobsearch():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    applications = load_applications(username)
    resumes = load_resumes(username)
    return render_template('jobsearch.html',
                           username=username,
                           applications=applications,
                           resumes=resumes)

# ─── API: Resume Library ────────────────────────────
@app.route('/api/resumes', methods=['GET', 'POST'])
def api_resumes():
    if 'username' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    username = session['username']
    if request.method == 'GET':
        return jsonify(load_resumes(username))
    data = request.json or {}
    data['id'] = str(int(_time.time() * 1000))
    resumes = load_resumes(username)
    resumes.append(data)
    save_resumes(username, resumes)
    return jsonify(data), 201

@app.route('/api/resumes/<rid>', methods=['PUT', 'DELETE'])
def api_resume_item(rid):
    if 'username' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    username = session['username']
    resumes = load_resumes(username)
    idx = next((i for i, r in enumerate(resumes) if str(r.get('id')) == rid), None)
    if idx is None:
        return jsonify({'error': 'not found'}), 404
    if request.method == 'PUT':
        data = request.json or {}
        data['id'] = rid
        resumes[idx] = data
        save_resumes(username, resumes)
        return jsonify(data)
    resumes.pop(idx)
    save_resumes(username, resumes)
    return jsonify({'ok': True})

# ─── API: Calendar Events ───────────────────────────
@app.route('/api/cal-events', methods=['GET', 'POST'])
def api_cal_events():
    if 'username' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    username = session['username']
    if request.method == 'GET':
        return jsonify(load_cal_events(username))
    data = request.json or {}
    data['id'] = str(int(_time.time() * 1000))
    events = load_cal_events(username)
    events.append(data)
    save_cal_events(username, events)
    return jsonify(data), 201

@app.route('/api/cal-events/<eid>', methods=['DELETE'])
def api_cal_event_item(eid):
    if 'username' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    username = session['username']
    events = [e for e in load_cal_events(username) if str(e.get('id')) != eid]
    save_cal_events(username, events)
    return jsonify({'ok': True})
@app.route('/settings')
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('settings.html', username=session['username'])
@app.route('/clear_applications', methods=['POST'])
def clear_applications():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    save_applications(username, [])
    return '', 204
# ─── Google OAuth ───────────────────────────────────
# To enable real Google login:
#   1. pip install authlib requests
#   2. Create a project at https://console.cloud.google.com
#   3. Enable OAuth 2.0, add redirect URI: http://localhost:5000/auth/google/callback
#   4. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET below
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')

@app.route('/auth/google')
def auth_google():
    if not GOOGLE_CLIENT_ID:
        # OAuth not configured — show notice and redirect back
        from flask import flash
        return redirect(url_for('login') + '?google_error=1')
    try:
        from authlib.integrations.flask_client import OAuth
        oauth = OAuth(app)
        google = oauth.register(
            name='google',
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={'scope': 'openid email profile'}
        )
        redirect_uri = url_for('auth_google_callback', _external=True)
        return google.authorize_redirect(redirect_uri)
    except ImportError:
        return redirect(url_for('login') + '?google_error=2')

@app.route('/auth/google/callback')
def auth_google_callback():
    if not GOOGLE_CLIENT_ID:
        return redirect(url_for('login'))
    try:
        from authlib.integrations.flask_client import OAuth
        oauth = OAuth(app)
        google = oauth.register(
            name='google',
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={'scope': 'openid email profile'}
        )
        token = google.authorize_access_token()
        userinfo = token.get('userinfo') or google.userinfo()
        email = userinfo.get('email', '')
        username = email.split('@')[0] if email else userinfo.get('sub', 'user')
        # Auto-register if not exists
        from src.auth import load_users, save_users
        users = load_users()
        if username not in users:
            users[username] = '__google__' + email
            save_users(users)
        session['username'] = username
        return redirect(url_for('welcome'))
    except Exception:
        return redirect(url_for('login') + '?google_error=3')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
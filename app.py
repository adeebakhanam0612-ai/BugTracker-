from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'bugtracker2026'
db = SQLAlchemy(app)

# ─── DATABASE MODELS ────────────────────────────────────────

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    project = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    assigned_to = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Open')
    date_reported = db.Column(db.String(50), nullable=False)

# ─── ROUTES ─────────────────────────────────────────────────

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['username'] = username
        session['role'] = role
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html', error="Invalid username or password!")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    total = Bug.query.count()
    open_bugs = Bug.query.filter_by(status='Open').count()
    resolved = Bug.query.filter_by(status='Resolved').count()
    in_progress = Bug.query.filter_by(status='In Progress').count()
    recent_bugs = Bug.query.order_by(Bug.id.desc()).limit(5).all()

    # Chart data
    high = Bug.query.filter_by(severity='High').count()
    medium = Bug.query.filter_by(severity='Medium').count()
    low = Bug.query.filter_by(severity='Low').count()

    sara_bugs = Bug.query.filter_by(assigned_to='Sara').count()
    adeeba_bugs = Bug.query.filter_by(assigned_to='Adeeba').count()
    juvairiya_bugs = Bug.query.filter_by(assigned_to='Juvairiya').count()

    return render_template('dashboard.html',
                           total=total,
                           open_bugs=open_bugs,
                           resolved=resolved,
                           in_progress=in_progress,
                           recent_bugs=recent_bugs,
                           high=high, medium=medium, low=low,
                           sara_bugs=sara_bugs,
                           adeeba_bugs=adeeba_bugs,
                           juvairiya_bugs=juvairiya_bugs)

@app.route('/bugreport')
def bugreport():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('bugreport.html')

@app.route('/submit_bug', methods=['POST'])
def submit_bug():
    title = request.form['title']
    project = request.form['project']
    description = request.form['description']
    severity = request.form['severity']
    assigned_to = request.form['assigned_to']
    date_reported = request.form['date_reported']
    new_bug = Bug(title=title, project=project,
                  description=description, severity=severity,
                  assigned_to=assigned_to,
                  date_reported=date_reported)
    db.session.add(new_bug)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/bugs')
def bugs():
    if 'username' not in session:
        return redirect(url_for('login'))
    search = request.args.get('search', '')
    severity_filter = request.args.get('severity', '')
    status_filter = request.args.get('status', '')
    query = Bug.query
    if search:
        query = query.filter(Bug.title.contains(search))
    if severity_filter:
        query = query.filter_by(severity=severity_filter)
    if status_filter:
        query = query.filter_by(status=status_filter)
    bugs = query.order_by(Bug.id.desc()).all()
    return render_template('bugs.html', bugs=bugs,
                           search=search,
                           severity_filter=severity_filter,
                           status_filter=status_filter)

@app.route('/update_status/<int:bug_id>', methods=['POST'])
def update_status(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    bug.status = request.form['status']
    db.session.commit()
    return redirect(url_for('bugs'))

@app.route('/productivity')
def productivity():
    if 'username' not in session:
        return redirect(url_for('login'))
    developers = ['Sara', 'Adeeba', 'Juvairiya']
    stats = []
    for dev in developers:
        assigned = Bug.query.filter_by(assigned_to=dev).count()
        resolved = Bug.query.filter_by(assigned_to=dev, status='Resolved').count()
        pending = Bug.query.filter_by(assigned_to=dev, status='Open').count()
        stats.append({
            'name': dev,
            'assigned': assigned,
            'resolved': resolved,
            'pending': pending
        })
    return render_template('productivity.html', stats=stats)

# ─── RUN ────────────────────────────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', password='1234', role='admin')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
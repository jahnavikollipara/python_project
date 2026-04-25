from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
import os
from datetime import datetime, timezone
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vault.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

db = SQLAlchemy(app)

# Load or generate encryption key
key_file = 'vault.key'
if os.path.exists(key_file):
    with open(key_file, 'rb') as f:
        key = f.read()
else:
    key = Fernet.generate_key()
    with open(key_file, 'wb') as f:
        f.write(key)

cipher = Fernet(key)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    encrypted_name = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('files', lazy=True))

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

def login_required(view):
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    wrapped_view.__name__ = view.__name__
    return wrapped_view

@app.route('/')
def index():
    if g.user:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
        else:
            user = User(username=username, email=email, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            flash('Account created successfully', 'success')
            return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    files = File.query.filter_by(user_id=g.user.id).all()
    return render_template('dashboard.html', username=g.user.username, files=files)

@app.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('dashboard'))
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('dashboard'))
    if file:
        filename = secure_filename(file.filename)
        file_data = file.read()
        encrypted_data = cipher.encrypt(file_data)
        encrypted_filename = f"{os.urandom(16).hex()}_{g.user.id}.enc"
        with open(os.path.join(app.config['UPLOAD_FOLDER'], encrypted_filename), 'wb') as f:
            f.write(encrypted_data)
        file_record = File(user_id=g.user.id, original_name=filename, encrypted_name=encrypted_filename, file_size=len(file_data))
        db.session.add(file_record)
        db.session.commit()
        flash('File uploaded successfully', 'success')
    return redirect(url_for('dashboard'))

@app.route('/download_file/<int:file_id>')
@login_required
def download_file(file_id):
    file_record = File.query.filter_by(id=file_id, user_id=g.user.id).first()
    if not file_record:
        flash('File not found', 'error')
        return redirect(url_for('dashboard'))
    with open(os.path.join(app.config['UPLOAD_FOLDER'], file_record.encrypted_name), 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = cipher.decrypt(encrypted_data)
    return send_file(io.BytesIO(decrypted_data), attachment_filename=file_record.original_name, as_attachment=True)

@app.route('/delete_file/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    file_record = File.query.filter_by(id=file_id, user_id=g.user.id).first()
    if not file_record:
        flash('File not found', 'error')
        return redirect(url_for('dashboard'))
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_record.encrypted_name))
    db.session.delete(file_record)
    db.session.commit()
    flash('File deleted successfully', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
import sqlite3

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Use secret key from environment

DATABASE = 'users.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Username already exists!"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
            if user:
                session['username'] = username
                return redirect(url_for('dashboard'))
            return "Invalid credentials!"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return f"Welcome to your dashboard, {session['username']}!"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    init_db()  # Initialize the database
    app.run(host='0.0.0.0', port=80)

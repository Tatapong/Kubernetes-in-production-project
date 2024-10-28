from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management and flashing messages

# In-memory storage for users
users = {}

@app.route('/')
def home():
    return render_template('index.html')  # Your home page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Simple validation
        if not username or not password:
            flash("Username and password are required!")
            return redirect(url_for('register'))

        if username in users:
            flash("Username already exists!")
            return redirect(url_for('register'))

        # Store the user in the in-memory dictionary
        users[username] = password
        flash("Registration successful!")
        return redirect(url_for('login'))  # Redirect to login or home page

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the user exists and the password matches
        if users.get(username) == password:
            flash("Login successful!")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))

    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

# pyrefly: ignore [missing-import]
import os
import json
from flask import Flask, request, render_template, redirect, url_for

# Initialize Flask app
# template_folder='.' means it will look for HTML files in the current directory
# static_folder='.' and static_url_path='' allows it to serve index.css and assets from the current directory
app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

# Define path to Users.json
USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Datasets', 'Users.json')

def load_users_raw():
    """
    Loads users from the JSON database in its raw format (list or dict).
    Does not overwrite on read failure, and defaults to dict format with admin user if empty.
    """
    if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
        # Default starting state: dictionary with admin
        default_data = {"admin": "admin"}
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        try:
            with open(USERS_FILE, 'w') as f:
                json.dump(default_data, f, indent=4)
        except IOError:
            pass
        return default_data
        
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading users database: {e}")
        # Return empty dictionary on decode error to prevent crashes, without overwriting the file
        return {}

def load_users():
    """
    Loads users and returns them normalized as a list of dicts: [{"username": "...", "password": "..."}].
    """
    raw = load_users_raw()
    if isinstance(raw, dict):
        return [{"username": k, "password": v} for k, v in raw.items()]
    elif isinstance(raw, list):
        return raw
    return []

def save_user(username, password):
    """
    Saves a user, preserving the original file format (dict or list).
    """
    raw = load_users_raw()
    if isinstance(raw, dict):
        raw[username] = password
    else:
        # If raw is a list or empty, treat as list
        if not isinstance(raw, list):
            raw = []
        raw.append({"username": username, "password": password})
        
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(raw, f, indent=4)
    except IOError as e:
        print(f"Error saving user to database: {e}")


@app.route('/')
def home():
    """
    Serves the main login page (index.html).
    """
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """
    Handles the login form submission.
    """
    # Retrieve username and password from the submitted form
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Load all users from JSON database
    users = load_users()
    
    # Check if username and password match any registered user
    for user in users:
        if user.get('username') == username and user.get('password') == password:
            return redirect(url_for('main_page'))
            
    # Redirect back to home with an error parameter
    return redirect(url_for('home', error='invalid'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Serves the signup page and handles signup form submission.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not password:
            return redirect(url_for('signup', error='invalid'))
            
        if password != confirm_password:
            return redirect(url_for('signup', error='mismatch'))
            
        # Check if username already exists
        users = load_users()
        for user in users:
            if user.get('username') == username:
                return redirect(url_for('signup', error='exists'))
                
        # Register user
        save_user(username, password)
        return redirect(url_for('home', success='registered'))
        
    return render_template('signup.html')

@app.route('/main')
def main_page():
    """
    Serves the main dashboard page (main.html).
    """
    return render_template('main.html')

if __name__ == '__main__':
    print("Starting FaceAttend Login Server...")
    print("Open your browser and navigate to: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)


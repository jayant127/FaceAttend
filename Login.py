from flask import Flask, request, render_template, redirect, url_for

# Initialize Flask app
# template_folder='.' means it will look for HTML files in the current directory
# static_folder='.' and static_url_path='' allows it to serve index.css and assets from the current directory
app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

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
    
    # Basic authentication logic for demonstration
    # Replace this with your actual database/authentication validation
    if username == "admin" and password == "admin":
        return "<h3>Login Successful!</h3><p>Welcome to FaceAttend.</p>" # Here you would redirect to the main app dashboard
    else:
        # For a real application, you would use flash messages and redirect back to login
        return "<h3>Login Failed!</h3><p>Invalid username or password. <a href='/'>Try again</a></p>"

if __name__ == '__main__':
    print("Starting FaceAttend Login Server...")
    print("Open your browser and navigate to: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)

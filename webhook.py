from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webhooks.db'
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    webhook_url = db.Column(db.String(200))

# Routes for user registration and login
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Handle registration form submission
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            return 'Username already exists'
        # Check if passwords match
        if password != confirm_password:
            return 'Passwords do not match'
        # Create a new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handle login form submission
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # Store user session or token for authentication
            return redirect(url_for('manage_hooks'))
        else:
            return 'Invalid username or password'
    return render_template('index.html')

@app.route('/manage_hooks', methods=['GET', 'POST'])
def manage_hooks():
    # Handle adding or updating webhook URL
    if request.method == 'POST':
        webhook_url = request.form['webhook_url']
        # Update the webhook URL for the logged-in user
        # You need to implement authentication to get the current user
        # current_user.webhook_url = webhook_url
        # db.session.commit()
        return redirect(url_for('manage_hooks'))
    # Generate a unique webhook URL for the user
    unique_webhook_url = f'https://smacforce.com/webhooks/{str(uuid.uuid4())}'
    # Pass the unique webhook URL to the template
    return render_template('manage_hooks.html', unique_webhook_url=unique_webhook_url)

# Route for receiving webhook requests
@app.route('/webhook/<username>', methods=['POST'])
def webhook(username):
    user = User.query.filter_by(username=username).first()
    if user:
        # Process the webhook payload
        payload = request.json
        # Store the payload in the database or perform actions
        return 'Webhook received successfully'
    else:
        return 'User not found', 404

if __name__ == '__main__':
    app.run(debug=True)

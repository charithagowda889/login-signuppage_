# Import required libraries from Flask and other packages
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy  # ORM to interact with database using Python classes
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from flask_cors import CORS


# Create Flask app instance
app = Flask(__name__, static_folder='static')
CORS(app)

# Configure database (SQLite file will be created as users.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Secret key used to sign JWT tokens (important for security)
app.config['JWT_SECRET_KEY'] = 'secret-key'

# Initialize database and JWT manager
db = SQLAlchemy(app)  # ORM setup
jwt = JWTManager(app)  # JWT authentication setup


# Define User model (table structure in database)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID
    username = db.Column(db.String(100), unique=True)  # Username must be unique
    password = db.Column(db.String(200))  # Stores hashed password
    role = db.Column(db.String(100))  # Optional user role
    location = db.Column(db.String(100))  # Optional location
    company = db.Column(db.String(100))  # Optional company

# Create database tables if not already created
with app.app_context():
    db.create_all()


# Route to serve frontend HTML file
@app.route('/')  # When user opens base URL
def serve_index():
    return send_from_directory('static', 'index.html')  # Returns index.html from static folder


# Signup API - creates new user
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json  # Get JSON data from request body

    # Check if username already exists in database
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'msg': 'User exists'}), 400

    # Create new user object with hashed password
    user = User(
        username=data['username'],
        password=generate_password_hash(data['password'])  # Securely hash password
    )

    # Save user to database
    db.session.add(user)
    db.session.commit()

    return jsonify({'msg': 'Signup successful'})  # Return success message


# Login API - authenticates user and returns JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.json  # Get request data

    # Fetch user by username
    user = User.query.filter_by(username=data['username']).first()

    # Check if user exists AND password is correct
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'msg': 'Invalid credentials'}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify(access_token=token)  # Send token to client


@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()  # Returns string (as we stored it)

    user = db.session.get(User, int(user_id))

    # Return user details
    return jsonify({
        'username': user.username,
        'role': user.role,
        'location': user.location,
        'company': user.company
    })


@app.route('/profile', methods=['POST'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))
    data = request.get_json()  # Get JSON data

    # Update fields only if present and not empty
    if 'role' in data and data['role']:
        user.role = data['role']

    if 'location' in data and data['location']:
        user.location = data['location']

    if 'company' in data and data['company']:
        user.company = data['company']

    # Save updated data
    db.session.commit()

    return jsonify({
        'msg': 'Profile updated',
        'username': user.username,
        'role': user.role,
        'location': user.location,
        'company': user.company
    })


# Run the Flask application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)  

from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'secret-key'

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(100))
    location = db.Column(db.String(100))
    company = db.Column(db.String(100))

with app.app_context():
    db.create_all()

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "User already exists"}), 400

    hashed = generate_password_hash(data['password'])

    user = User(username=data['username'], password=hashed)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Signup successful"})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'msg': 'Invalid credentials'}), 401
    token = create_access_token(identity=str(user.id))
    return jsonify(access_token=token)

@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user = User.query.get(get_jwt_identity())
    return jsonify({
        'username': user.username,
        'role': user.role,
        'location': user.location,
        'company': user.company
    })

@app.route('/profile', methods=['POST'])
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    data = request.get_json()

    
    if 'role' in data and data['role']:
        user.role = data['role']

    if 'location' in data and data['location']:
        user.location = data['location']

    if 'company' in data and data['company']:
        user.company = data['company']

    db.session.commit()

    return jsonify({"msg": "Profile updated"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

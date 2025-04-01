from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId
import bcrypt
import os
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/aqi_prediction")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your-secret-key-here")
mongo = PyMongo(app)

# JWT token decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            token = token.split(" ")[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = mongo.db.users.find_one({'_id': ObjectId(data['user_id'])})
            if not current_user:
                return jsonify({'message': 'Invalid token!'}), 401
        except:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if required fields are present
    if not all(k in data for k in ["username", "email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Check if user already exists
    if mongo.db.users.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already registered"}), 400
    
    if mongo.db.users.find_one({"username": data["username"]}):
        return jsonify({"error": "Username already taken"}), 400
    
    # Hash the password
    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
    
    # Create new user
    user = {
        "username": data["username"],
        "email": data["email"],
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }
    
    try:
        mongo.db.users.insert_one(user)
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Check if required fields are present
    if not all(k in data for k in ["email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Find user by email
    user = mongo.db.users.find_one({"email": data["email"]})
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Check password
    if bcrypt.checkpw(data["password"].encode('utf-8'), user["password"]):
        # Generate JWT token
        token = jwt.encode({
            'user_id': str(user['_id']),
            'exp': datetime.utcnow() + timedelta(days=1)
        }, app.config['SECRET_KEY'])
        
        return jsonify({
            "token": token,
            "user": {
                "id": str(user["_id"]),
                "username": user["username"],
                "email": user["email"]
            }
        }), 200
    
    return jsonify({"error": "Invalid email or password"}), 401

@app.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify({
        "username": current_user["username"],
        "email": current_user["email"],
        "created_at": current_user["created_at"]
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
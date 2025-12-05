"""  
ATS Backend System (Python/Flask)
Converted from Node.js Express
- Configuration & Imports
- Database Models (Job, Candidate, User)
- Domain Logic / Services
- Controllers & Routes
- Server Initialization
"""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from functools import wraps
import logging

# ===== 1. CONFIGURATION =====

app = Flask(__name__)
CORS(app)

# Configuration
PORT = os.getenv('PORT', 3000)
MONGO_URI = 'mongodb+srv://atsadmin:ATS@1234!@cluster0.mojt7bbg.mongodb.net/?appName=Cluster0'
DB_NAME = 'ats_db'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

# ===== 2. MONGODB CONNECTION =====

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[DB_NAME]
    
    # Test connection
    client.admin.command('ping')
    logger.info('✅ MongoDB Connected')
    
    # Get collections
    users_collection = db['users']
    candidates_collection = db['candidates']
    jobs_collection = db['jobs']
    
    # Ensure indexes
    users_collection.create_index('username', unique=True)
    users_collection.create_index('email', unique=True)
    
except Exception as err:
    logger.error(f'❌ MongoDB Connection Error: {err}')
    exit(1)

# ===== 3. DATABASE MODELS / SCHEMAS =====

class User:
    def __init__(self, username, email, password, fullName, userType):
        self.username = username
        self.email = email
        self.password = password  # In production, hash this with bcrypt
        self.fullName = fullName
        self.userType = userType  # 'job_seeker' or 'recruiter'
        self.createdAt = datetime.now()
    
    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'fullName': self.fullName,
            'userType': self.userType,
            'createdAt': self.createdAt
        }

# ===== 4. HELPER FUNCTIONS =====

def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc and '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

def validate_required_fields(data, required_fields):
    """Validate that all required fields are present"""
    missing = [f for f in required_fields if not data.get(f)]
    return missing

# ===== 5. ROUTES - STATIC FILES =====

@app.route('/')
def serve_root():
    """Serve root directory"""
    return send_from_directory('.', 'register.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static HTML files"""
    if filename.endswith('.html'):
        return send_from_directory('.', filename)
    return 'Not Found', 404

# ===== 6. ROUTES - AUTHENTICATION =====

@app.route('/api/auth/register', methods=['POST'])
def register():
    """
    Register Route - Create new user
    POST /api/auth/register
    """
    try:
        data = request.get_json()
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        fullName = data.get('fullName')
        userType = data.get('userType', 'job_seeker')
        
            logger.info(f'📝 Register Request Received: username={username}, email={email}, password=****, fullName={fullName}, userType={userType}')
        # Validation
        if not all([username, email, password]):
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        # Check if user already exists
        existing_user = users_collection.find_one({
            '$or': [{'username': username}, {'email': email}]
        })
        
        if existing_user:
            return jsonify({'error': 'Username or email already exists'}), 400
        
        # Create new user
        new_user = User(username, email, password, fullName, userType)
        result = users_collection.insert_one(new_user.to_dict())
        
        logger.info(f'✅ User saved successfully: {result.inserted_id}')
        
        return jsonify({
            'message': 'User registered successfully',
            'userId': str(result.inserted_id)
        }), 201
    
    except Exception as err:
        logger.error(f'❌ Registration Error: {str(err)}')
        logger.error(f'Full Error: {err}')
        return jsonify({'error': str(err)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    Login Route - Authenticate user
    POST /api/auth/login
    """
    try:
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        
        # Validation
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        logger.info(f'📝 Login attempt for username: {username}')
        
        # Find user
        user = users_collection.find_one({'username': username})
        logger.info(f'User found: {"Yes" if user else "No"}')
        
        if not user:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Check password (in production, use bcrypt.compare())
        if user['password'] != password:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Return user data (in production, return a JWT token)
        return jsonify({
            'message': 'Login successful',
            'user': {
                '_id': str(user['_id']),
                'username': user['username'],
                'email': user['email'],
                'fullName': user['fullName'],
                'userType': user['userType']
            }
        }), 200
    
    except Exception as err:
        logger.error(f'❌ Login Error: {str(err)}')
        return jsonify({'error': str(err)}), 500

# ===== 7. ERROR HANDLERS =====

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

# ===== 8. SERVER INITIALIZATION =====

if __name__ == '__main__':
    logger.info(f'🚀 Server running on port {PORT}')
    app.run(
        host='127.0.0.1',
        port=PORT,
        debug=True
    )

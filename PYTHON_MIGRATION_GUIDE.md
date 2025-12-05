# Node.js to Python/Flask Migration Guide

## Overview
Your ATS (Applicant Tracking System) backend has been successfully converted from **Node.js/Express** to **Python/Flask**.

### What Changed?

| Aspect | Node.js | Python |
|--------|---------|--------|
| **Framework** | Express.js | Flask |
| **Database Driver** | Mongoose | PyMongo |
| **File** | backend.js | app.py |
| **Port** | 3000 | 3000 (same) |
| **Entry Point** | npm start | python app.py |

---

## Prerequisites

Before running the Python backend, ensure you have:

1. **Python 3.8+** installed on your system
   ```bash
   python --version  # or python3 --version
   ```

2. **pip** (Python package manager) installed
   ```bash
   pip --version  # or pip3 --version
   ```

---

## Installation & Setup

### Step 1: Create Virtual Environment (Recommended)
Creating a virtual environment keeps dependencies isolated:

```bash
# Windows
python -m venv venv
venv\\Scripts\\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- **Flask** - Web framework
- **Flask-CORS** - Cross-Origin Resource Sharing support  
- **PyMongo** - MongoDB driver
- **python-dotenv** - Environment variable management

---

## Running the Server

### Option 1: Run Directly
```bash
python app.py
```

You should see:
```
✅ MongoDB Connected
🚀 Server running on port 3000
```

### Option 2: Run with Flask CLI
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

---

## Accessing the Application

Once the server is running, access it at:

```
http://127.0.0.1:3000/register.html
```

### Available Endpoints

#### 1. Register User
```
POST /api/auth/register
Content-Type: application/json

{
  "username": "testuser123",
  "email": "test@example.com",
  "password": "password123",
  "fullName": "Test User",
  "userType": "job_seeker"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "userId": "507f1f77bcf86cd799439011"
}
```

#### 2. Login User
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "testuser123",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "_id": "507f1f77bcf86cd799439011",
    "username": "testuser123",
    "email": "test@example.com",
    "fullName": "Test User",
    "userType": "job_seeker"
  }
}
```

---

## Key Code Differences

### Express Route vs Flask Route

**Express.js (backend.js):**
```javascript
app.post('/api/auth/register', async (req, res) => {
  const { username, email, password } = req.body;
  // logic here
  res.status(201).json({ message: 'Success' });
});
```

**Flask (app.py):**
```python
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    # logic here
    return jsonify({'message': 'Success'}), 201
```

### MongoDB Operations

**Mongoose (Node.js):**
```javascript
const user = await User.findOne({ username });
const result = await newUser.save();
```

**PyMongo (Python):**
```python
user = users_collection.find_one({'username': username})
result = users_collection.insert_one(new_user.to_dict())
```

---

## Debugging

### Enable Debug Logging
The Python backend includes comprehensive logging. Check the console output for:

```
📝 Register Request Received: {...}
✅ User saved successfully: ObjectId(...)
❌ Registration Error: [error details]
🚀 Server running on port 3000
```

### Common Issues

**Issue: "ModuleNotFoundError: No module named 'flask'"**
- Solution: Run `pip install -r requirements.txt`

**Issue: "MongoDB Connection Error"**
- Solution: Verify MongoDB Atlas connection string in `app.py` line 27
- Check that your IP is whitelisted in MongoDB Atlas
- Ensure MongoDB cluster is active

**Issue: "Address already in use"**
- Solution: Port 3000 is already in use. Either:
  - Stop the process using that port
  - Or change PORT in `app.py` line 25

---

## Database (MongoDB Atlas)

### Connection String
The backend connects to your MongoDB Atlas cluster:
```
mongodb+srv://atsadmin:ATS@1234!@cluster0.mojt7bbg.mongodb.net/?appName=Cluster0
```

### Database Structure
- **Database**: `ats_db`
- **Collections**:
  - `users` - User accounts (with unique indexes on `username` and `email`)
  - `jobs` - Job listings (for future use)
  - `candidates` - Candidate profiles (for future use)

---

## Frontend (HTML Files)

The Python Flask server automatically serves HTML files from the current directory:

- `http://127.0.0.1:3000/register.html` - User registration
- `http://127.0.0.1:3000/login.html` - User login

No changes needed to your HTML files! They work exactly the same way.

---

## Next Steps

### 1. Add Password Hashing
Replace plain-text password storage with bcrypt:

```bash
pip install bcrypt
```

Then in `app.py`:
```python
import bcrypt

# When saving:
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# When checking:
bcrypt.checkpw(password.encode(), user['password'])
```

### 2. Add JWT Authentication
For secure token-based authentication:

```bash
pip install PyJWT
```

### 3. Add Input Validation
Use validation libraries for better security:

```bash
pip install Flask-Validator
```

### 4. Environment Variables
Create a `.env` file for sensitive data:

```
MONGO_URI=mongodb+srv://atsadmin:ATS@1234!@cluster0.mojt7bbg.mongodb.net/?appName=Cluster0
PORT=3000
FLASK_ENV=development
```

---

## Production Deployment

### Using Gunicorn
For production, use Gunicorn (production-grade WSGI server):

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 app:app
```

### Deployment Platforms
- **Heroku**: `git push heroku main`
- **PythonAnywhere**: Upload files and configure WSGI
- **AWS/GCP/Azure**: Use their Python runtime support

---

## Comparison: Node.js vs Python

### Advantages of Python/Flask Version
✅ Simpler syntax - easier to read and maintain  
✅ Fewer dependencies - lighter weight  
✅ Better for data processing - great for future ML integration  
✅ Large ecosystem - thousands of libraries available  

### Equivalent Features
✅ CORS support - works exactly like Express  
✅ JSON responses - same format  
✅ MongoDB integration - same database driver  
✅ Static file serving - serves HTML files  
✅ Error handling - comprehensive error responses  

---

## Troubleshooting

For detailed debugging, check the backend console output. The Python version includes extensive logging:

```
[DEBUG] Login attempt for username: testuser123
[DEBUG] User found: Yes
[INFO] ✅ User saved successfully
[ERROR] ❌ Registration Error: [details]
```

---

## Support

If you encounter issues:

1. Check MongoDB Atlas connection
2. Verify all dependencies are installed (`pip list`)
3. Review error messages in console output
4. Ensure Python 3.8+ is being used
5. Try creating a fresh virtual environment

---

**Migration completed successfully! Your ATS backend is now running on Python/Flask.**

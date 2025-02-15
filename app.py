from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from agent import simple_agent, automator_agent, openai_agent
## API Setup

app = Flask(__name__)

# Database file path (stored locally)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create the database (if not exists)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "Flask app with SQLite is running!"})

### App Logic

@app.route('/run', methods=['POST'])
def run_task():
    task = request.args.get('task')
    if not task:
        return jsonify({"error": "Missing task parameter"}), 400
    
    try:
        # Here you would implement your task execution logic
        # For now, we'll just return a placeholder response

        # simple_agent();
        result = automator_agent(task);
        # openai_agent();


        return jsonify({
            "status": "success",
            "task": task,
            "result": result
        }), 200
    except ValueError as e:
        return jsonify({
            "error": "Task execution failed",
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route('/read', methods=['GET'])
def read_file():
    file_path = request.args.get('path')
    if not file_path:
        return jsonify({"error": "Missing path parameter"}), 400

    # Ensure the path is safe and within the project directory
    try:
        # Normalize the path and ensure it's within the project directory
        abs_path = os.path.abspath(file_path)
        if not abs_path.startswith(os.path.dirname(BASE_DIR)):
            return jsonify({"error": "Access denied: Path outside project directory"}), 403
        
        if not os.path.exists(abs_path):
            return "", 404
        
        with open(abs_path, 'r') as file:
            content = file.read()
            return content, 200, {'Content-Type': 'text/plain'}
            
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

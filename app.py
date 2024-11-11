from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import requests


app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# WeatherAPI key
API_KEY = "b05247a56acd4aaf809152649240511"

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)

# Initialize the database if it doesn’t exist
if not os.path.exists('tasks.db'):
    with app.app_context():
        db.create_all()

# Render HTML template with tasks
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('todo.html', tasks=tasks)

# JSON API Routes

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "completed": task.completed
    } for task in tasks])

# Add a new task (JSON request)
@app.route('/tasks', methods=['POST'])
def add_task_json():
    data = request.json
    title = data.get('title')
    description = data.get('description', '')
    due_date_str = data.get('due_date')
    
    if due_date_str:
        due_date = datetime.fromisoformat(due_date_str)
    else:
        due_date = None
    
    new_task = Task(
        title=title,
        description=description,
        due_date=due_date,
        completed=False
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created successfully", "task_id": new_task.id}), 201

# Update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    due_date_str = data.get('due_date')
    
    if due_date_str:
        task.due_date = datetime.fromisoformat(due_date_str)
    
    db.session.commit()
    return jsonify({"message": "Task updated successfully"}), 200

# Toggle task completion
@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def toggle_complete_task_json(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    task.completed = not task.completed
    db.session.commit()
    return jsonify({"message": f"Task marked as {'completed' if task.completed else 'incomplete'}"}), 200

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_json(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully."}), 204
    return jsonify({"error": "Task not found."}), 404

# Get weather info for a task location (assuming latitude and longitude are provided in query params)
@app.route('/weather/<int:task_id>', methods=['GET'])
def get_weather(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    
    if not latitude or not longitude:
        return jsonify({"error": "Latitude and longitude are required"}), 400
    
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={latitude},{longitude}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather_info = {
                "temperature": data['current']['temp_c'],
                "condition": data['current']['condition']['text'],
                "location": data['location']['name'],
                "region": data['location']['region'],
                "country": data['location']['country']
            }
            return jsonify(weather_info)
        else:
            return jsonify({"error": "Could not fetch weather data"}), 500
    except Exception as e:
        return jsonify({"error": "Request failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database Initialization
DB_NAME = "tasks.db"

def init_db():
    """Initialize the SQLite database and create tasks table if not exists."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()

# Utility function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

@app.route('/')
def home():
    return "Welcome to the To-Do List API with SQLite!"

@app.route('/tasks', methods=['POST'])
def add_task():
    """Add a new task to the database."""
    data = request.json
    title = data.get("title", "")
    if not title:
        return {"error": "Title is required"}, 400
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, completed) VALUES (?, ?)", (title, False))
        conn.commit()
        task_id = cursor.lastrowid
    return jsonify({"id": task_id, "title": title, "completed": False}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update the completed status of a task."""
    data = request.json
    completed = data.get("completed", None)
    if completed is None:
        return {"error": "Completed status is required"}, 400

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
        conn.commit()
        if cursor.rowcount == 0:
            return {"error": "Task not found"}, 404
    
    return jsonify({"id": task_id, "completed": completed}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by its ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return {"error": "Task not found"}, 404
    
    return '', 204

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Retrieve all tasks."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = [dict(row) for row in cursor.fetchall()]
    return jsonify(tasks), 200

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(host='0.0.0.0', port=5000, debug=True)

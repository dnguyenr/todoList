from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory database
tasks = []

@app.route('/')
def home():
    return "Welcome to the To-Do List API!"

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    task = {"id": len(tasks) + 1, "title": data["title"], "completed": False}
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = data["completed"]
            return jsonify(task)
    return {"error": "Task not found"}, 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

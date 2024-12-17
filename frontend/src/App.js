import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://192.168.0.41:5000'; // for flask

function App() {
    const [tasks, setTasks] = useState([]);
    const [newTask, setNewTask] = useState('');
 
    const addTask = () => {
        axios.post(`${API_URL}/tasks`, { title: newTask }).then((response) => {
            setTasks([...tasks, response.data]);
            setNewTask('');
        });
    };

    const toggleTask = (id, completed) => {
        axios.put(`${API_URL}/tasks/${id}`, { completed: !completed }).then((response) => {
            setTasks(tasks.map((task) => (task.id === id ? response.data : task)));
        });
    };

    const deleteTask = (id) => {
        axios.delete(`${API_URL}/tasks/${id}`).then(() => {
            setTasks(tasks.filter((task) => task.id !== id));
        });
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>To-Do List</h1>
            <input
                type="text"
                value={newTask}
                onChange={(e) => setNewTask(e.target.value)}
                placeholder="New Task"
            />
            <button onClick={addTask}>Add Task</button>
            <ul>
                    {tasks.map((task) => (
                        <li key={task.id}>
                            <span
                                style={{
                                    textDecoration: task.completed ? 'line-through' : 'none',
                                    cursor: 'pointer',
                                }}
                                onClick={() => toggleTask(task.id, task.completed)}
                            >
                                {task.title}
                            </span>
                            <button onClick={() => deleteTask(task.id)}>Delete</button>
                        </li>
                    ))}
                </ul>
        </div>
    );
}

export default App;

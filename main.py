from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB (Assuming MongoDB is running locally)
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['todo_db']  # Database
todos = db['todos']     # Collection

# Home route
@app.route('/')
def home():
    return "Welcome to the To-Do List API!"

# 1. Create a new To-Do item (POST Request)
@app.route('/todo', methods=['POST'])
def add_todo():
    data = request.json  # Get data from request
    task = {
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'status': 'pending'
    }
    todos.insert_one(task)
    return jsonify({'msg': 'Task created successfully', 'task': task}), 201

# 2. Get all To-Do items (GET Request)
@app.route('/todos', methods=['GET'])
def get_all_todos():
    tasks = []
    for task in todos.find():
        task['_id'] = str(task['_id'])  # Convert ObjectId to string
        tasks.append(task)
    return jsonify(tasks), 200

# 3. Get a specific To-Do item by ID (GET Request)
@app.route('/todo/<id>', methods=['GET'])
def get_todo_by_id(id):
    task = todos.find_one({'_id': ObjectId(id)})
    if task:
        task['_id'] = str(task['_id'])  # Convert ObjectId to string
        return jsonify(task), 200
    else:
        return jsonify({'msg': 'Task not found'}), 404

# 4. Update a To-Do item (PUT Request)
@app.route('/todo/<id>', methods=['PUT'])
def update_todo(id):
    data = request.json
    updated_task = {
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'status': data.get('status', 'pending')
    }
    result = todos.update_one({'_id': ObjectId(id)}, {'$set': updated_task})
    
    if result.matched_count:
        return jsonify({'msg': 'Task updated successfully'}), 200
    else:
        return jsonify({'msg': 'Task not found'}), 404

# 5. Delete a To-Do item (DELETE Request)
@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    result = todos.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'msg': 'Task deleted successfully'}), 200
    else:
        return jsonify({'msg': 'Task not found'}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

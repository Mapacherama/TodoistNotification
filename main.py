from flask import Flask, redirect, request, jsonify
import requests
import Todoist_notifications

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome! Please <a href="/login">login</a>.'

@app.route('/login')
def login():
    return redirect(f"{Todoist_notifications.AUTHORIZATION_URL}?response_type=code&client_id={Todoist_notifications.CLIENT_ID}&redirect_uri={Todoist_notifications.REDIRECT_URI}")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    
    token_data = {
        'client_id': Todoist_notifications.CLIENT_ID,
        'client_secret': Todoist_notifications.CLIENT_SECRET,
        'code': code,
        'redirect_uri': Todoist_notifications.REDIRECT_URI
    }
    
    response = requests.post(Todoist_notifications.TOKEN_URL, data=token_data)
    token_data = response.json()
    access_token = token_data.get('access_token')
    
    Todoist_notifications.set_access_token(access_token)
    
    return f'Access Token: {access_token}'

@app.route('/tasks', methods=['POST'])
def create_task():
    content = request.json.get('content')
    due_date = request.json.get('due_date')
    Todoist_notifications.create_task(content, due_date)
    return jsonify({"message": "Task created successfully."}), 201

@app.route('/tasks', methods=['GET'])
def read_tasks():
    tasks = Todoist_notifications.read_tasks()
    return jsonify(tasks), 200

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    content = request.json.get('content')
    Todoist_notifications.update_task(task_id, content)
    return jsonify({"message": "Task updated successfully."}), 200

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    Todoist_notifications.delete_task(task_id)
    return jsonify({"message": "Task deleted successfully."}), 204

if __name__ == '__main__':
    app.run(port=5000)

from quart import Quart, redirect, request, jsonify
import requests
import Todoist_notifications
from flasgger import Swagger

app = Quart(__name__)
swagger = Swagger(app)

@app.route('/')
async def home():
    return 'Welcome! Please <a href="/login">login</a>.'

@app.route('/login')
def login():
    scope = "data:read_write"
    return redirect(f"{Todoist_notifications.AUTHORIZATION_URL}?response_type=code&client_id={Todoist_notifications.CLIENT_ID}&redirect_uri={Todoist_notifications.REDIRECT_URI}&scope={scope}")

@app.route('/callback')
async def callback():
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
async def create_task():
    """
    Create a new task
    ---
    parameters:
      - name: content
        in: body
        type: string
        required: true
      - name: due_date
        in: body
        type: string
        required: false
    responses:
      201:
        description: Task created successfully
    """
    content = (await request.get_json()).get('content')
    due_date = (await request.get_json()).get('due_date')
    Todoist_notifications.create_task(content, due_date)
    return jsonify({"message": "Task created successfully."}), 201

@app.route('/tasks', methods=['GET'])
async def read_tasks():
    """
    Get all tasks
    ---
    responses:
      200:
        description: A list of tasks
    """
    tasks = Todoist_notifications.read_tasks()
    return jsonify(tasks), 200

@app.route('/tasks/<task_id>', methods=['PUT'])
async def update_task(task_id):
    """
    Update a task
    ---
    parameters:
      - name: task_id
        in: path
        type: string
        required: true
      - name: content
        in: body
        type: string
        required: true
    responses:
      200:
        description: Task updated successfully
    """
    content = (await request.get_json()).get('content')
    Todoist_notifications.update_task(task_id, content)
    return jsonify({"message": "Task updated successfully."}), 200

@app.route('/tasks/<task_id>', methods=['DELETE'])
async def delete_task(task_id):
    """
    Delete a task
    ---
    parameters:
      - name: task_id
        in: path
        type: string
        required: true
    responses:
      204:
        description: Task deleted successfully
    """
    Todoist_notifications.delete_task(task_id)
    return jsonify({"message": "Task deleted successfully."}), 204

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)
import requests
import time
from plyer import notification
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import threading
import json

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/callback'
AUTHORIZATION_URL = 'https://todoist.com/oauth/authorize'
TOKEN_URL = 'https://todoist.com/oauth/access_token'
TODOIST_API_URL = "https://api.todoist.com/rest/v2/tasks"

access_token = None

def set_access_token(token):
    global access_token
    access_token = token

@app.get("/")
async def home():
    auth_url = (
        f"{AUTHORIZATION_URL}?client_id={CLIENT_ID}&scope=data:read_write&state=random_state_string&redirect_uri={REDIRECT_URI}"
    )
    return RedirectResponse(url=auth_url)

@app.get("/callback")
async def callback(code: str):
    print("Current working directory:", os.getcwd())
    # Store the code in a JSON file
    with open('oauth_code.json', 'w') as code_file:
        json.dump({"oauth_code": code}, code_file)

    token_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    token_response = requests.post(TOKEN_URL, data=token_data)

    if token_response.status_code != 200:
        print(f"Error retrieving access token: {token_response.text}")
        return {"error": "Failed to retrieve access token"}

    token_json = token_response.json()
    access_token = token_json.get('access_token')

    if access_token:
        try:
            with open('token.json', 'w') as token_file:
                json.dump({"access_token": access_token}, token_file)
            print("Access token saved to token.json")
        except Exception as e:
            print(f"Error writing token to file: {e}")
    else:
        print("Access token not found in response.")

    return {"access_token": access_token}

def fetch_todays_tasks():
    global access_token

    if not access_token:
        print("No access token. Authenticate via OAuth first.")
        return []

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(TODOIST_API_URL, headers=headers)
        tasks = response.json()
        today_tasks = [task for task in tasks if task.get('due') and task['due']['date'] == time.strftime("%Y-%m-%d")]
        return today_tasks
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return []

def notify(task):
    notification.notify(
        title="Task Reminder",
        message=f"Task: {task['content']}\nDue: {task['due']['date']}",
        timeout=10
    )

def main_task_checker():
    print("Checking today's tasks...")
    tasks = fetch_todays_tasks()

    if tasks:
        for task in tasks:
            notify(task)
    else:
        print("No tasks due today.")

def start_fastapi_app():
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)

def create_task(content, due_date=None):
    global access_token
    if not access_token:
        print("No access token. Authenticate via OAuth first.")
        return

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    task_data = {
        "content": content,
        "due": {"date": due_date} if due_date else None
    }

    response = requests.post(TODOIST_API_URL, headers=headers, data=json.dumps(task_data))
    if response.status_code == 200:
        print("Task created successfully.")
    else:
        print(f"Error creating task: {response.text}")

def read_tasks():
    global access_token
    if not access_token:
        print("No access token. Authenticate via OAuth first.")
        return []

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(TODOIST_API_URL, headers=headers)
    if response.status_code == 200:
        tasks = response.json()
        return tasks
    else:
        print(f"Error fetching tasks: {response.text}")
        return []

def update_task(task_id, content):
    global access_token
    if not access_token:
        print("No access token. Authenticate via OAuth first.")
        return

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    update_data = {
        "content": content
    }

    response = requests.post(f"{TODOIST_API_URL}/{task_id}", headers=headers, data=json.dumps(update_data))
    if response.status_code == 204:
        print("Task updated successfully.")
    else:
        print(f"Error updating task: {response.text}")

def delete_task(task_id):
    global access_token
    if not access_token:
        print("No access token. Authenticate via OAuth first.")
        return

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.delete(f"{TODOIST_API_URL}/{task_id}", headers=headers)
    if response.status_code == 204:
        print("Task deleted successfully.")
    else:
        print(f"Error deleting task: {response.text}")

if __name__ == "__main__":
    access_token = None
    threading.Thread(target=start_fastapi_app).start()

    while not access_token:
        print("Waiting for OAuth token... Please visit http://localhost:5000 to authenticate.")
        time.sleep(5)

    main_task_checker()

    create_task("Test Task", "2024-12-31")
    tasks = read_tasks()
    print(tasks)

    # Example of updating a task (replace 'task_id' with an actual task ID)
    # update_task(task_id, "Updated Task Content")

    # Example of deleting a task (replace 'task_id' with an actual task ID)
    # delete_task(task_id)

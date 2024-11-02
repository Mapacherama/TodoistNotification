import requests
import time
from plyer import notification
from flask import Flask, request, redirect
import threading

app = Flask(__name__)

CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'http://localhost:5000/callback'
AUTHORIZATION_URL = 'https://todoist.com/oauth/authorize'
TOKEN_URL = 'https://todoist.com/oauth/access_token'
TODOIST_API_URL = "https://api.todoist.com/rest/v2/tasks"

access_token = None

def set_access_token(token):
    global access_token
    access_token = token

@app.route('/')
def home():
    auth_url = (
        f"{AUTHORIZATION_URL}?client_id={CLIENT_ID}&scope=data:read_write&state=random_state_string&redirect_uri={REDIRECT_URI}"
    )
    return redirect(auth_url)

@app.route('/callback')
def callback():
    global access_token
    code = request.args.get('code')

    token_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    token_response = requests.post(TOKEN_URL, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    return f"Access token obtained: {access_token}"

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

def start_flask_app():
    app.run(port=5000)

if __name__ == "__main__":
    access_token = None
    threading.Thread(target=start_flask_app).start()

    while not access_token:
        print("Waiting for OAuth token... Please visit http://localhost:5000 to authenticate.")
        time.sleep(5)

    main_task_checker()

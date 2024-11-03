from todoist_api_python.api import TodoistAPI
import os
import json
from dotenv import load_dotenv
import time

load_dotenv()

TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN")
api = TodoistAPI(TODOIST_API_TOKEN)

def read_tasks():
    try:
        tasks = api.get_tasks()
        print("Raw tasks response:", tasks) 
        return tasks
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return []

def create_task(content: str, due_date: str = None):
    try:
        new_task = api.add_task(content=content, due_date=due_date)
        return new_task
    except Exception as e:
        print(f"Error creating task: {e}")
        return {"error": str(e)}

def update_task(task_id: str, content: str):
    try:
        api.update_task(task_id, content=content)
        return {"message": "Task updated successfully."}
    except Exception as e:
        print(f"Error updating task: {e}")
        return {"error": str(e)}

def delete_task(task_id: str):
    try:
        api.delete_task(task_id)
        return {"message": "Task deleted successfully."}
    except Exception as e:
        print(f"Error deleting task: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    access_token = None
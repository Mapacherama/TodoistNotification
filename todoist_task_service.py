from todoist_api_python.api import TodoistAPI
import os
import json
from dotenv import load_dotenv
import time
from datetime import datetime

load_dotenv()

TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN")
api = TodoistAPI(TODOIST_API_TOKEN)

def read_tasks(filter_criteria="p1"):
    try:
        tasks = api.get_tasks()
        filtered_tasks = [
            task for task in tasks
            if (filter_criteria == "p1" and task.priority == 1) or
               (filter_criteria == "today" and task.due and task.due.date == datetime.today().strftime("%Y-%m-%d"))
        ]
        print("Filtered tasks:", filtered_tasks)
        return filtered_tasks
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return {"error": str(e)}

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
from todoist_api_python.api import TodoistAPI
import os
import json
from dotenv import load_dotenv
import time
from datetime import datetime
from fastapi import HTTPException
import requests

load_dotenv()

TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN")
api = TodoistAPI(TODOIST_API_TOKEN)

class SpotifyService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def notify_playback(self, track_uri: str, play_time: str):
        spotify_url = f"{self.base_url}/schedule-playlist"
        
        params = {
            "playlist_uri": track_uri,
            "play_time": datetime.strptime(play_time, "%Y-%m-%dT%H:%M:%S%z").strftime("%H:%M")
        }

        try:
            response = requests.get(spotify_url, params=params)
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to schedule Spotify playback")

        except Exception as e:
            raise HTTPException(status_code=500, detail="Error scheduling Spotify playback")

# Initialize SpotifyService
spotify_service = SpotifyService(base_url="http://127.0.0.1:8000")

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

def schedule_spotify_playback(track_uri: str, play_time: str):
    spotify_service.notify_playback(track_uri, play_time)

if __name__ == "__main__":
    access_token = None
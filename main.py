from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

import todoist_task_service

load_dotenv()
TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskCreate(BaseModel):
    content: str
    due_date: str = None
    track_uri: str = None
    play_time: str = None

class TaskUpdate(BaseModel):
    content: str

@app.post("/tasks", response_model=dict)
async def create_task(task: TaskCreate):
    new_task = todoist_task_service.create_task(task.content, task.due_date)
    if "error" in new_task:
        raise HTTPException(status_code=400, detail=new_task["error"])

    if task.track_uri and task.play_time:
        try:
            todoist_task_service.schedule_spotify_playback(task.track_uri, task.play_time)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    return {"message": "Task created successfully.", "task": new_task}

@app.get("/tasks", response_model=list)
async def read_tasks(filter_criteria: str = Query("p1", description="Filter criteria like 'p1' for high priority or 'today' for tasks due today")):
    tasks = todoist_task_service.read_tasks(filter_criteria)
    if "error" in tasks:
        raise HTTPException(status_code=400, detail=tasks["error"])
    return tasks

@app.put("/tasks/{task_id}", response_model=dict)
async def update_task(task_id: str, task: TaskUpdate):
    result = todoist_task_service.update_task(task_id, task.content)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: str):
    result = todoist_task_service.delete_task(task_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)
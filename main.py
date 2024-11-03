from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN")

# Initialize Todoist API client
api = TodoistAPI(TODOIST_API_TOKEN)

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

class TaskUpdate(BaseModel):
    content: str

@app.post("/tasks", response_model=dict)
async def create_task(task: TaskCreate):
    try:
        new_task = api.add_task(content=task.content, due_date=task.due_date)
        return {"message": "Task created successfully.", "task": new_task}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/tasks", response_model=list)
async def read_tasks():
    try:
        tasks = api.get_tasks()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/tasks/{task_id}", response_model=dict)
async def update_task(task_id: str, task: TaskUpdate):
    try:
        api.update_task(task_id, content=task.content)
        return {"message": "Task updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: str):
    try:
        api.delete_task(task_id)
        return {"message": "Task deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)
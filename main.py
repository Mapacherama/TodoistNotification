from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import Todoist_notifications

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
    Todoist_notifications.create_task(task.content, task.due_date)
    return {"message": "Task created successfully."}

@app.get("/tasks", response_model=list)
async def read_tasks():
    tasks = Todoist_notifications.read_tasks()
    return tasks

@app.put("/tasks/{task_id}", response_model=dict)
async def update_task(task_id: str, task: TaskUpdate):
    Todoist_notifications.update_task(task_id, task.content)
    return {"message": "Task updated successfully."}

@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: str):
    Todoist_notifications.delete_task(task_id)
    return {"message": "Task deleted successfully."}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import requests
import Todoist_notifications

app = FastAPI()

# Pydantic models for request validation
class TaskCreate(BaseModel):
    content: str
    due_date: str = None

class TaskUpdate(BaseModel):
    content: str

@app.get("/")
async def home():
    return {"message": "Welcome! Please login."}

@app.get("/login")
async def login():
    scope = "data:read_write"
    return RedirectResponse(url=f"{Todoist_notifications.AUTHORIZATION_URL}?response_type=code&client_id={Todoist_notifications.CLIENT_ID}&redirect_uri={Todoist_notifications.REDIRECT_URI}&scope={scope}")

@app.get("/callback")
async def callback(code: str):
    token_data = {
        'client_id': Todoist_notifications.CLIENT_ID,
        'client_secret': Todoist_notifications.CLIENT_SECRET,
        'code': code,
        'redirect_uri': Todoist_notifications.REDIRECT_URI
    }
    
    response = requests.post(Todoist_notifications.TOKEN_URL, data=token_data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve access token")

    token_data = response.json()
    access_token = token_data.get('access_token')
    
    if access_token:
        Todoist_notifications.set_access_token(access_token)
    else:
        raise HTTPException(status_code=400, detail="Access token not found in response")

    return {"access_token": access_token}

@app.post("/tasks", response_model=dict)
async def create_task(task: TaskCreate):
    """
    Create a new task
    """
    Todoist_notifications.create_task(task.content, task.due_date)
    return {"message": "Task created successfully."}

@app.get("/tasks", response_model=list)
async def read_tasks():
    """
    Get all tasks
    """
    tasks = Todoist_notifications.read_tasks()
    return tasks

@app.put("/tasks/{task_id}", response_model=dict)
async def update_task(task_id: str, task: TaskUpdate):
    """
    Update a task
    """
    Todoist_notifications.update_task(task_id, task.content)
    return {"message": "Task updated successfully."}

@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: str):
    """
    Delete a task
    """
    Todoist_notifications.delete_task(task_id)
    return {"message": "Task deleted successfully."}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer
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

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="http://localhost:5000/authenticate",
    tokenUrl="http://localhost:5000/callback"
)

class TaskCreate(BaseModel):
    content: str
    due_date: str = None

class TaskUpdate(BaseModel):
    content: str

@app.get("/authenticate", summary="Authenticate Todoist", tags=["Auth"])
def todoist_authenticate():
    auth_url = Todoist_notifications.authenticate_todoist()
    print("Redirecting to Todoist for authentication...")
    print(f"Authorization URL: {auth_url}")
    
    return RedirectResponse(url=auth_url)

@app.get("/callback")
async def callback(code: str):
    token_json = await Todoist_notifications.authenticate(code)
    
    if "error" in token_json:
        raise HTTPException(status_code=400, detail=token_json["error"])

    access_token = token_json.get('access_token')
    
    if access_token:
        Todoist_notifications.set_access_token(access_token)
    else:
        raise HTTPException(status_code=400, detail="Access token not found in response")

    return {"access_token": access_token}

@app.post("/tasks", response_model=dict)
async def create_task(task: TaskCreate):
    Todoist_notifications.create_task(task.content, task.due_date)
    return {"message": "Task created successfully."}

@app.get("/tasks", response_model=list)
async def read_tasks(token: str = Depends(oauth2_scheme)):
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
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel
import requests
import Todoist_notifications

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TODOIST_API_URL = "https://api.todoist.com/rest/v2/tasks"

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

@app.get("/proxy/todoist")
async def proxy_todoist_api():
    global access_token

    if not access_token:
        raise HTTPException(status_code=401, detail="No access token. Authenticate via OAuth first.")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(TODOIST_API_URL, headers=headers)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=response.status_code, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)
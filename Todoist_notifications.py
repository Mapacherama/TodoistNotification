from todoist_api_python.api import TodoistAPI
import os
import json
from dotenv import load_dotenv
import time

load_dotenv()

TODOIST_TOKEN = os.getenv("TODOIST_API_TOKEN")
REDIRECT_URI = os.getenv("REDIRECT_URI")
api = TodoistAPI(TODOIST_TOKEN)

def set_access_token(token):
    global access_token
    access_token = token

async def authenticate(code: str):
    try:
        token_json = api.get_access_token(code)
        access_token = token_json.get('access_token')
        set_access_token(access_token)

        if access_token:
            with open('token.json', 'w') as token_file:
                json.dump({"access_token": access_token}, token_file)
            print("Access token saved to token.json")
        else:
            print("Access token not found in response.")
    except Exception as e:
        print(f"Error retrieving access token: {e}")
        return {"error": "Failed to retrieve access token"}

    return {"access_token": access_token}

def authenticate_todoist():
    scope = "data:read_write"
    auth_url = f"{api.get_authorization_url(redirect_uri=REDIRECT_URI, scope=scope)}"
    return auth_url

if __name__ == "__main__":
    access_token = None

    while not access_token:
        print("Waiting for OAuth token... Please visit http://localhost:5000 to authenticate.")
        time.sleep(5)

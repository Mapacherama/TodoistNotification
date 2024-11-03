from todoist_api_python.api import TodoistAPI
import os
import json
from dotenv import load_dotenv
import time

load_dotenv()

TODOIST_TOKEN = os.getenv("TODOIST_API_TOKEN")
REDIRECT_URI = os.getenv("REDIRECT_URI")
api = TodoistAPI(TODOIST_TOKEN)

if __name__ == "__main__":
    access_token = None

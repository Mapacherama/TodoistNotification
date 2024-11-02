from flask import Flask, redirect, request
import requests
import Todoist_notifications  # Import your Todoist notifications module

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome! Please <a href="/login">login</a>.'

@app.route('/login')
def login():
    return redirect(f"{Todoist_notifications.AUTHORIZATION_URL}?response_type=code&client_id={Todoist_notifications.CLIENT_ID}&redirect_uri={Todoist_notifications.REDIRECT_URI}")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_data = {
        'client_id': Todoist_notifications.CLIENT_ID,
        'client_secret': Todoist_notifications.CLIENT_SECRET,
        'code': code,
        'redirect_uri': Todoist_notifications.REDIRECT_URI
    }
    
    response = requests.post(Todoist_notifications.TOKEN_URL, data=token_data)
    token_data = response.json()
    access_token = token_data.get('access_token')
    
    Todoist_notifications.set_access_token(access_token)
    
    return f'Access Token: {access_token}'

if __name__ == '__main__':
    app.run(port=5000)

# TodoistNotification

## Overview
TodoistNotification is a FastAPI application that integrates with the Todoist API to manage tasks and send notifications for due tasks. It implements OAuth authentication to securely access the Todoist API and provides endpoints for creating, reading, updating, and deleting tasks.

## Features
- OAuth authentication with Todoist
- Fetch today's tasks and send reminders
- Create, read, update, and delete tasks
- CORS support for cross-origin requests
- Notifications for task reminders using plyer

## Requirements
- Python 3.7+
- FastAPI
- Uvicorn
- Requests
- Plyer
- python-dotenv

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TodoistNotification.git
   cd TodoistNotification
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Todoist API credentials:
   ```plaintext
   CLIENT_ID=your_client_id
   CLIENT_SECRET=your_client_secret
   ```

## Usage
1. Start the FastAPI application:
   ```bash
   python main.py
   ```

2. Visit `http://localhost:5000/docs` to access the Swagger UI and interact with the API.

3. Authenticate with Todoist by visiting `http://localhost:5000/` to initiate the OAuth flow.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
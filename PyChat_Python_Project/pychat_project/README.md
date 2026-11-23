# PyChat – Python Web Chat Application

PyChat is a beginner-friendly browser-based group chat application built with Python and Flask. Users choose a display name, join a shared room, send messages and see new messages appear automatically.

## Features
- Username-based joining (no account registration required)
- Shared general chat room
- Message history stored in SQLite
- Automatic message refresh every two seconds
- Responsive interface for desktop and mobile
- Basic input validation and safe text rendering
- Health-check endpoint at `/health`

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment:
   - Windows: `py -m venv venv` then `venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv venv` then `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the application: `python app.py`
6. Open `http://127.0.0.1:5000` in your browser.

## Deploy on Render
1. Create a GitHub account and a new repository named `pychat`.
2. Upload the contents of this folder to that repository.
3. Sign in to Render and choose **New > Web Service**.
4. Connect your GitHub repository. Render can use the included `render.yaml`; otherwise set build command to `pip install -r requirements.txt` and start command to `gunicorn app:app`.
5. Deploy. Render will provide a public `onrender.com` URL.

## Notes and limitations
This is an educational demonstration, not a production-secure messaging service. It uses a shared public room, username-only identity, and polling rather than WebSockets. The default SQLite file may not persist across some hosting restarts or redeployments unless a persistent disk/database is configured. Do not use it for private or sensitive conversations. Set a strong `SECRET_KEY` in the deployment environment.

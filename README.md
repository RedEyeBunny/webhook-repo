# Webhook Receiver with Flask and MongoDB

This Flask app receives GitHub webhook events (`push` and `pull_request`) and displays them on a UI that refreshes every 15 seconds.

## Features
- Webhook endpoint at `/webhook`
- Stores events in MongoDB
- Frontend displays real-time updates via polling (`/events` API)
- Supports:
  - Push
  - Pull Requests

## Setup
1. Run MongoDB (Docker or local)
2. Install dependencies: `pip install -r requirements.txt`
3. Start the app: `python app.py`
4. Expose via ngrok: `ngrok http 5000`

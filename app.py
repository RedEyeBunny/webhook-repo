from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime


app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["webhook_db"]
collection = db["github_events"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/webhook', methods=['POST'])
def webhook():
    event = request.headers.get('X-GitHub-Event')
    payload = request.json

    try:
        if event == 'push':
            data = {
                "author": payload["pusher"]["name"],
                "to_branch": payload["ref"].split("/")[-1],
                "timestamp": datetime.utcnow().isoformat(),
                "action": "push"
            }
        elif event == 'pull_request':
            pr = payload["pull_request"]
            data = {
                "author": pr["user"]["login"],
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": pr["created_at"],
                "action": "pull_request"
            }
        else:
            return jsonify({"status": "ignored"}), 200

        collection.insert_one(data)
        return jsonify({"status": "stored"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find().sort("timestamp", -1).limit(10))
    for event in events:
        event['_id'] = str(event['_id'])
    return jsonify(events)

if __name__ == '__main__':
    app.run(port=5000)

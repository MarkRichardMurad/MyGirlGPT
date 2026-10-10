from flask import Flask, request, jsonify
import os
import json
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "MyGirlGPT API is running"

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    return jsonify({
        "reply": f"Echo: {message}",
        "status": "ok"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

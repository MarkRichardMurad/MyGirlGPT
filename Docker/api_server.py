from flask import Flask, request, jsonify
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
SYSTEM_PROMPT = os.getenv(
    "CHARACTER_PROMPT",
    "You are MyGirlGPT, a warm, supportive, flirtatious, emotionally intelligent AI companion. "
    "Speak naturally, concisely, and with personality. Keep the conversation engaging and affectionate, "
    "but remain respectful and safe."
)

@app.route("/")
def home():
    return "MyGirlGPT API is running"

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        message = (data.get("message") or "").strip()

        if not message:
            return jsonify({"error": "message is required"}), 400

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            temperature=0.9,
            max_tokens=400,
        )

        reply = completion.choices[0].message.content
        return jsonify({
            "reply": reply,
            "status": "ok",
            "model": MODEL_NAME,
        })

    except Exception as exc:
        app.logger.exception("OpenAI chat request failed")
        return jsonify({
            "error": "Failed to generate response",
            "details": str(exc),
            "status": "error"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

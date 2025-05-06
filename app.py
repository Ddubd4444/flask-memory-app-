from flask import Flask, request, jsonify, render_template_string
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["100 per minute"])

PHRASE_FILE = "phrase_scroll.json"

# Load phrases from file or start with empty list
if os.path.exists(PHRASE_FILE):
    with open(PHRASE_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = []

@app.route("/", methods=["GET"])
def index():
    return render_template_string("""
        <h1>Your Flask server is alive!</h1>
        <form method="POST" action="/save">
            <input type="text" name="phrase" placeholder="Enter a phrase" required>
            <input type="text" name="tone" placeholder="Enter a tone (optional)">
            <button type="submit">Save Phrase</button>
        </form>
        <p>👉 <a href="/memory">Click here to view all stored phrases</a></p>
    """)

@app.route("/save", methods=["POST"])
def save_phrase():
    phrase = request.form.get("phrase")
    tone = request.form.get("tone", "")

    if phrase:
        memory.append({"phrase": phrase, "tone": tone})
        with open(PHRASE_FILE, "w") as f:
            json.dump(memory, f, indent=2)
    return render_template_string("""
        <p>✅ Saved. <a href="/">Back</a></p>
    """)

@app.route("/memory", methods=["GET"])
def view_memory():
    return jsonify(memory)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

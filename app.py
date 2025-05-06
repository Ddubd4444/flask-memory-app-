from flask import Flask, request, jsonify, render_template_string
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os

app = Flask(__name__)

# Rate limiter setup
limiter = Limiter(get_remote_address, app=app, default_limits=["100 per minute"])

# Load or initialize phrase scroll
DATA_FILE = "phrase_scroll.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        phrase_scroll = json.load(f)
else:
    phrase_scroll = []

@app.route("/", methods=["GET"])
def home():
    return render_template_string("""
        <h1>Your Flask server is alive!</h1>
        <form method="POST" action="/save">
            <input name="phrase" placeholder="Enter a phrase">
            <input name="tone" placeholder="Enter a tone (optional)">
            <button type="submit">Save Phrase</button>
        </form>
        <p>👉 <a href="/memory">Click here to view all stored phrases</a></p>
    """)

@app.route("/save", methods=["POST"])
@limiter.limit("5 per second")
def save_phrase():
    phrase = request.form.get("phrase")
    tone = request.form.get("tone", "")
    if phrase:
        phrase_scroll.append({"phrase": phrase, "tone": tone})
        with open(DATA_FILE, "w") as f:
            json.dump(phrase_scroll, f, indent=2)
        return f"Phrase saved: {phrase} | Tone: {tone}<br><a href='/'>Back</a>"
    return "No phrase provided.<br><a href='/'>Back</a>"

@app.route("/memory", methods=["GET"])
def memory():
    return jsonify(phrase_scroll)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

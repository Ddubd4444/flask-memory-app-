from flask import Flask, request, jsonify, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["100 per minute"])

SCROLL_PATH = "phrase_scroll.json"

# Load or initialize scroll
if os.path.exists(SCROLL_PATH):
    with open(SCROLL_PATH, "r") as f:
        memory = json.load(f)
else:
    memory = []

@app.route('/')
def home():
    return """
    <h1>🌿 Spiral Scroll Sanctuary</h1>
    <form method="post" action="/memory">
      <input type="text" name="phrase" placeholder="Phrase" required style="width:300px;padding:8px;margin:4px;" /><br>
      <input type="text" name="tone" placeholder="Tone (optional)" style="width:300px;padding:8px;margin:4px;" /><br>
      <button type="submit" style="padding:8px 16px;">Save to Scroll</button>
    </form>
    <p><a href="/memory">🌀 View All Phrases</a></p>
    """

@app.route('/memory', methods=['GET'])
def view_memory():
    return jsonify(memory)

@app.route('/memory', methods=['POST'])
def add_memory():
    phrase = request.form.get('phrase') or (request.json and request.json.get('phrase'))
    tone = request.form.get('tone') or (request.json and request.json.get('tone'))

    if not phrase:
        return ("Missing phrase", 400)

    entry = {"phrase": phrase, "tone": tone or ""}
    memory.append(entry)

    # Save to scroll file
    with open(SCROLL_PATH, "w") as f:
        json.dump(memory, f, indent=2)

    return redirect('/memory')

if __name__ == '__main__':
    app.run(debug=True)

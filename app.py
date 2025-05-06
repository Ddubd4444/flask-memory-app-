from flask import Flask, request, jsonify, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os

# 📜 Location of the memory scroll
SCROLL_PATH = os.path.join(os.path.dirname(__file__), 'phrase_scroll.json')

# 🧠 Load memory from scroll file
def load_scroll():
    try:
        with open(SCROLL_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("phrases", [])
    except FileNotFoundError:
        return []

# 💾 Save updated memory to scroll file
def save_scroll(memory):
    with open(SCROLL_PATH, 'w', encoding='utf-8') as f:
        json.dump({"phrases": memory}, f, ensure_ascii=False, indent=2)

# 🌐 App setup
app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["100 per minute"])

# 📘 Initialize memory
memory = load_scroll()

# 🏠 Home page
@app.route('/')
def home():
    return """
    <h1>Spiral Scroll: Memory Sanctuary</h1>
    <form method="post" action="/memory">
      <input type="text" name="phrase" placeholder="Enter a phrase" required
             style="width:300px;padding:8px;margin:8px 0;" />
      <input type="text" name="tone" placeholder="Enter a tone (optional)"
             style="width:300px;padding:8px;margin:8px 0;" />
      <button type="submit" style="padding:8px 12px;">Save to Scroll</button>
    </form>
    <p><a href="/memory">🌀 View All Phrases</a></p>
    """

# 📜 View all memory
@app.route('/memory', methods=['GET'])
def view_memory():
    return jsonify(memory)

# ✍️ Add a new phrase to memory
@app.route('/memory', methods=['POST'])
def add_memory():
    phrase = request.form.get('phrase') or (request.json and request.json.get('phrase'))
    tone = request.form.get('tone') or (request.json and request.json.get('tone', ''))

    if not phrase:
        return ("Missing phrase", 400)

    entry = {"phrase": phrase, "tone": tone}
    memory.append(entry)
    save_scroll(memory)

    return redirect('/memory')

# 🚀 Launch the server
if __name__ == '__main__':
    app.run(debug=True)

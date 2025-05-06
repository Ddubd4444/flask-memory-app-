from flask import Flask, request, jsonify, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 1️⃣ — App setup
app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["100 per minute"])

# 2️⃣ — In-memory memory space
memory = []

# 3️⃣ — Home page with phrase + tone form
@app.route('/')
def home():
    return """
    <h1>Your Flask server is alive!</h1>
    <form method="post" action="/memory">
      <input type="text" name="phrase" placeholder="Enter a phrase" required
             style="width:300px;padding:8px;margin:8px 0;" />
      <input type="text" name="tone" placeholder="Enter a tone (optional)"
             style="width:200px;padding:8px;margin:8px 0;" />
      <button type="submit" style="padding:8px 12px;">Save Phrase</button>
    </form>
    <p>👉 <a href="/memory">Click here to view all stored phrases</a></p>
    """

# 4️⃣ — View stored phrases + tones
@app.route('/memory', methods=['GET'])
def view_memory():
    return jsonify(memory)

# 5️⃣ — Add a new memory (phrase + tone)
@app.route('/memory', methods=['POST'])
def add_memory():
    phrase = request.form.get('phrase') or (request.json and request.json.get('phrase'))
    tone = request.form.get('tone') or (request.json and request.json.get('tone'))

    if not phrase:
        return ("Missing phrase", 400)

    memory.append({"phrase": phrase, "tone": tone})
    return redirect('/memory')

# 6️⃣ — Start the app
if __name__ == '__main__':
    app.run(debug=True)

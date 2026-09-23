"""Shared-room teaching demo: SQLite history and HTTP polling, no user accounts."""
import os
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)
app.config['CHAT_DATABASE'] = os.environ.get('CHAT_DATABASE', str(Path(app.instance_path) / 'chat.sqlite'))

def connect():
    path = Path(app.config['CHAT_DATABASE'])
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    db.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, room TEXT NOT NULL, name TEXT NOT NULL, text TEXT NOT NULL)')
    return db

@app.get('/')
def index():
    return 'Chat API is running. Open the Vite URL to use the React app.'

@app.route('/api/messages', methods=['GET', 'POST'])
def messages():
    data = request.get_json(silent=True) if request.method == 'POST' else request.args
    if data is None or not hasattr(data, 'get'):
        return jsonify(error='Invalid request'), 400
    room = data.get('room', '')
    if not isinstance(room, str) or not room.strip() or len(room) > 40:
        return jsonify(error='Room must have 1–40 characters'), 400
    room = room.strip()
    if request.method == 'POST':
        # JSON-only writes reject ordinary cross-site HTML form submissions.
        name, text = data.get('name'), data.get('text')
        if not isinstance(name, str) or not name.strip() or len(name) > 30 or not isinstance(text, str) or not text.strip() or len(text) > 500:
            return jsonify(error='Name: 1–30 characters; message: 1–500 characters'), 400
        with connect() as db:
            db.execute('INSERT INTO messages(room,name,text) VALUES (?,?,?)', (room, name.strip(), text.strip()))
            db.execute('DELETE FROM messages WHERE room=? AND id NOT IN (SELECT id FROM messages WHERE room=? ORDER BY id DESC LIMIT 100)', (room, room))
        return jsonify(ok=True), 201
    with connect() as db:
        rows = db.execute('SELECT id,name,text FROM messages WHERE room=? ORDER BY id', (room,)).fetchall()
    return jsonify([dict(row) for row in rows])

if __name__ == '__main__':
    app.run(port=5001)

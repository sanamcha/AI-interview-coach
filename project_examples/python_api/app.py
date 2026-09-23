"""Python performs the API requests; JavaScript renders the returned data."""
import json
import os
import secrets
import ssl
import certifi
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from flask import Flask, jsonify, render_template, request
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
CSRFProtect(app)
API = 'https://jsonplaceholder.typicode.com/posts'

@app.get('/')
def index():
    return render_template('index.html')

@app.route('/api/posts', methods=['GET', 'POST'])
@app.route('/api/posts/<int:item_id>', methods=['PATCH', 'DELETE'])
def posts(item_id=None):
    method = request.method
    payload = None
    if method in ('POST', 'PATCH'):
        data = request.get_json(silent=True)
        title = data.get('title') if isinstance(data, dict) else None
        if not isinstance(title, str) or not title.strip() or len(title.strip()) > 120:
            return jsonify(error='Title must have 1–120 characters'), 400
        payload = {'title': title.strip()}
        if method == 'POST':
            payload.update(body='', userId=1)
    url = API + (f'/{item_id}' if item_id is not None else '')
    if method == 'GET':
        url += '?_limit=20'
    upstream = Request(url, method=method,
                       data=json.dumps(payload).encode() if payload is not None else None,
                       headers={'Content-Type': 'application/json', 'User-Agent': 'InterviewCoach-CRUD-Demo'})
    try:
        with urlopen(upstream, timeout=12, context=ssl.create_default_context(cafile=certifi.where())) as response:
            result = json.load(response) if method != 'DELETE' else {}
        return jsonify(result), 201 if method == 'POST' else 200
    except (HTTPError, URLError, TimeoutError, ValueError):
        return jsonify(error='Demo API unavailable. Please retry.'), 502

if __name__ == '__main__':
    app.run(port=5001)

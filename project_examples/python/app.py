"""Local Flask To-Do tutorial. Tasks live in a signed browser session cookie."""
import os
import secrets

from flask import Flask, abort, redirect, render_template, request, session, url_for
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    tasks = session.get('tasks', [])
    error = None
    if request.method == 'POST':
        text = request.form.get('task', '').strip()
        if not text or len(text) > 120:
            error = 'Enter a task between 1 and 120 characters.'
        elif len(tasks) >= 10:
            error = 'This small demo supports 10 tasks. Delete one first.'
        else:
            tasks.append({'id': secrets.token_hex(8), 'text': text, 'done': False})
            session['tasks'] = tasks
            return redirect(url_for('index'))
    return render_template('index.html', tasks=tasks, error=error)


@app.post('/tasks/<task_id>/<action>')
def update(task_id, action):
    if action not in ('toggle', 'delete'):
        abort(404)
    tasks = session.get('tasks', [])
    task = next((item for item in tasks if item['id'] == task_id), None)
    if task is None:
        abort(404)
    if action == 'toggle':
        task['done'] = not task['done']
    else:
        tasks = [item for item in tasks if item['id'] != task_id]
    session['tasks'] = tasks
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=5001)

"""Flask star rating with server-rendered buttons and a per-browser session."""
import os
import secrets
from flask import Flask, abort, redirect, render_template, request, session, url_for
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
CSRFProtect(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        value = request.form.get('rating', type=int)
        if value not in range(1, 6):
            abort(400)
        session['rating'] = 0 if session.get('rating', 0) == value else value
        return redirect(url_for('index'))
    return render_template('index.html', rating=session.get('rating', 0))

if __name__ == '__main__':
    app.run(port=5001)

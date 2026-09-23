import os
import random
import secrets
from flask import Flask, redirect, render_template, request, session, url_for
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
CSRFProtect(app)
YES_QUESTIONS = ['Do you enjoy reading books?', 'Do you like trying new foods?', 'Do you enjoy outdoor walks?', 'Do you like listening to music?', 'Would you like to learn a new language?']
TEXT_QUESTIONS = ['What is your favorite hobby?', 'Which place would you like to visit?', 'What would you like to learn next?']

def start():
    session['questions'] = random.sample(YES_QUESTIONS, 2) + [random.choice(TEXT_QUESTIONS)]
    session['answers'] = ['', '', '']

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'questions' not in session:
        start()
    answers = session['answers']
    first_missing = next((i for i, value in enumerate(answers) if not value), 2)
    step = max(0, min(request.args.get('step', 0, type=int), first_missing, 2))
    error = None
    if request.method == 'POST':
        value = request.form.get('answer', '').strip()
        if not value or len(value) > 200 or (step < 2 and value not in ('Yes', 'No')):
            error = 'Please provide a valid answer (up to 200 characters).'
        else:
            answers[step] = value
            session['answers'] = answers
            return redirect(url_for('results') if step == 2 else url_for('index', step=step + 1))
    return render_template('index.html', step=step, question=session['questions'][step], answer=answers[step], error=error)

@app.get('/results')
def results():
    answers = session.get('answers', [])
    if len(answers) != 3 or not all(answers):
        return redirect(url_for('index'))
    return render_template('results.html', results=list(zip(session['questions'], answers)))

@app.post('/restart')
def restart():
    start()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5001)

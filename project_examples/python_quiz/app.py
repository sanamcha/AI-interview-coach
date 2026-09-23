"""Five-question randomized quiz; answers and score are checked on the server."""
import os
import random
import secrets
from flask import Flask, redirect, render_template, request, session, url_for
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
CSRFProtect(app)
BANK = [{'question': 'What is 6 × 7?', 'choices': ['36', '42', '48'], 'correct': 1}, {'question': 'Which planet is closest to the Sun?', 'choices': ['Venus', 'Earth', 'Mercury'], 'correct': 2}, {'question': 'How many sides does a triangle have?', 'choices': ['3', '4', '5'], 'correct': 0}, {'question': 'Which animal is a mammal?', 'choices': ['Shark', 'Dolphin', 'Trout'], 'correct': 1}, {'question': 'What is the capital of France?', 'choices': ['Rome', 'Madrid', 'Paris'], 'correct': 2}, {'question': 'How many minutes are in an hour?', 'choices': ['60', '100', '30'], 'correct': 0}, {'question': 'Which language runs natively in web browsers?', 'choices': ['Python', 'JavaScript', 'Java'], 'correct': 1}, {'question': 'What does HTML describe?', 'choices': ['Database queries', 'Network encryption', 'Web page structure'], 'correct': 2}, {'question': 'What is 15 + 8?', 'choices': ['23', '21', '25'], 'correct': 0}, {'question': 'Which is a primary color of light?', 'choices': ['Brown', 'Red', 'Orange'], 'correct': 1}]

def start():
    session['question_ids'] = random.sample(range(len(BANK)), 5)
    session['answers'] = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'question_ids' not in session:
        start()
    answers = session['answers']
    if len(answers) == 5:
        return redirect(url_for('results'))
    step = len(answers)
    question = BANK[session['question_ids'][step]]
    error = None
    if request.method == 'POST':
        # Reject stale or duplicate submissions without scoring twice.
        if request.form.get('step', type=int) != step:
            return redirect(url_for('index'))
        answer = request.form.get('answer', type=int)
        if answer not in range(len(question['choices'])):
            error = 'Choose an answer before continuing.'
        else:
            session['answers'] = answers + [answer]
            return redirect(url_for('results') if step == 4 else url_for('index'))
    return render_template('index.html', question=question, step=step, error=error)

@app.get('/results')
def results():
    answers = session.get('answers', [])
    if len(answers) != 5:
        return redirect(url_for('index'))
    questions = [BANK[i] for i in session['question_ids']]
    score = sum(answer == question['correct'] for question, answer in zip(questions, answers))
    return render_template('results.html', score=score, percentage=score * 100 // 5,
                           review=list(zip(questions, answers)))

@app.post('/restart')
def restart():
    start()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5001)

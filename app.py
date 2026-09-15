"""Interview Coach: a small Flask app for interview practice."""

import json
import os
import secrets

from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import func

from forms import (AnswerForm, DeleteAttemptForm, FeedbackPracticeForm,
                   GuestLoginForm, LoginForm, SignupForm)
from models import Attempt, Question, User, db
from python_questions import PYTHON_QUESTIONS
from sql_questions import SQL_QUESTIONS
from behavioral_questions import BEHAVIORAL_QUESTIONS
from react_questions import REACT_QUESTIONS
from web_questions import CSS_QUESTIONS, HTML_QUESTIONS, JAVASCRIPT_QUESTIONS
from data_science_questions import DATA_SCIENCE_QUESTIONS

CURR_USER_KEY = 'current_user_id'
FEEDBACK_TOPICS = {
    'python': ('Python', PYTHON_QUESTIONS),
    'sql': ('SQL', SQL_QUESTIONS),
    'behavioral': ('Behavioral', BEHAVIORAL_QUESTIONS),
    'react': ('React', REACT_QUESTIONS),
    'html': ('HTML', HTML_QUESTIONS),
    'css': ('CSS', CSS_QUESTIONS),
    'javascript': ('JavaScript', JAVASCRIPT_QUESTIONS),
    'data-science': ('Data Science', DATA_SCIENCE_QUESTIONS),
}

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'change-me-before-deploying'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'postgresql+psycopg:///interview_coach'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db.init_app(app)


@app.before_request
def load_logged_in_user():
    user_id = session.get(CURR_USER_KEY)
    g.user = db.session.get(User, user_id) if user_id else None


def login_user(user):
    session[CURR_USER_KEY] = user.id


def fallback_feedback(answer):
    """Useful local feedback when an OpenAI key is not configured."""
    word_count = len(answer.split())
    score = min(90, max(40, 35 + word_count // 3))
    notes = []
    if word_count < 75:
        notes.append('Add more detail and include one concrete example.')
    if not any(word in answer.lower() for word in ('result', 'impact', 'improved', 'learned')):
        notes.append('End by explaining the result or what you learned.')
    if not notes:
        notes.append('Clear answer. Make the first sentence even more direct in a real interview.')
    return score, ' '.join(notes), 'local coach'


def get_feedback(question, answer):
    """Use OpenAI only when a key is configured; otherwise use local feedback."""
    if not os.environ.get('OPENAI_API_KEY'):
        return fallback_feedback(answer)
    try:
        from openai import OpenAI
        client = OpenAI()
        response = client.responses.create(
            model=os.environ.get('OPENAI_MODEL', 'gpt-5'),
            instructions=(
                'You are a supportive interview coach. Return JSON only with '
                'score (an integer from 0 to 100) and feedback (under 100 words).'
            ),
            input='Interview question:\n{}\n\nCandidate answer:\n{}'.format(question.text, answer),
            max_output_tokens=250,
            store=False,
        )
        data = json.loads(response.output_text)
        return max(0, min(100, int(data['score']))), str(data['feedback']), 'AI coach'
    except Exception:
        return fallback_feedback(answer)


def login_required():
    if not g.user:
        flash('Please log in to continue.', 'warning')
        return False
    return True


@app.route('/')
def home():
    if g.user:
        return redirect(url_for('dashboard'))
    return render_template('home.html', guest_form=GuestLoginForm())


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if g.user:
        return redirect(url_for('dashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            form.username.errors.append('That username is already taken.')
        elif User.query.filter_by(email=form.email.data.lower()).first():
            form.email.errors.append('That email is already registered.')
        else:
            user = User(username=form.username.data, email=form.email.data.lower())
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form, guest_form=GuestLoginForm())


@app.post('/guest-login')
def guest_login():
    """Create a random guest account and sign it in immediately."""
    if g.user:
        return redirect(url_for('dashboard'))

    form = GuestLoginForm()
    if not form.validate_on_submit():
        abort(400)

    token = secrets.token_hex(6)
    guest = User(
        username='guest_{}'.format(token),
        email='guest_{}@example.invalid'.format(token),
    )
    guest.set_password(secrets.token_urlsafe(32))
    db.session.add(guest)
    db.session.commit()
    login_user(guest)
    flash('You are practicing as a guest. Create an account to keep access on another device.', 'success')
    return redirect(url_for('dashboard'))


@app.post('/logout')
def logout():
    session.pop(CURR_USER_KEY, None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():
    if not login_required():
        return redirect(url_for('login'))
    attempts = (Attempt.query.filter_by(user_id=g.user.id)
                .order_by(Attempt.created_at.desc()).limit(10).all())
    database_categories = [row[0] for row in db.session.query(Question.category)
                           .distinct().order_by(Question.category)]
    categories = list(dict.fromkeys(['Python', 'SQL', 'Behavioral', 'React', 'HTML', 'CSS', 'JavaScript', 'Data Science'] + database_categories))
    average = round(sum(item.score for item in attempts) / len(attempts)) if attempts else None
    return render_template('dashboard.html', attempts=attempts,
                           categories=categories, average=average,
                           delete_form=DeleteAttemptForm())


@app.route('/my-feedback')
def my_feedback():
    """Show the full saved-answer history for the signed-in user."""
    if not login_required():
        return redirect(url_for('login'))
    attempts = (Attempt.query.filter_by(user_id=g.user.id)
                .order_by(Attempt.created_at.desc()).all())
    return render_template('my_feedback.html', attempts=attempts,
                           delete_form=DeleteAttemptForm())


@app.route('/python-interview-questions')
def python_interview_questions():
    """Show the Python question library with answers hidden by default."""
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=PYTHON_QUESTIONS,
                           library_title='100 common Python interview questions',
                           library_label='PYTHON STUDY LIBRARY', feedback_topic='python')


@app.route('/sql-interview-questions')
def sql_interview_questions():
    """Show the SQL question library with answers hidden by default."""
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=SQL_QUESTIONS,
                           library_title='100 common SQL interview questions',
                           library_label='SQL STUDY LIBRARY', feedback_topic='sql')


@app.route('/behavioral-interview-questions')
def behavioral_interview_questions():
    """Show behavioral prompts with hidden STAR-answer guidance."""
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=BEHAVIORAL_QUESTIONS,
                           library_title='50 common behavioral interview questions',
                           library_label='BEHAVIORAL STUDY LIBRARY', feedback_topic='behavioral')


@app.route('/react-interview-questions')
def react_interview_questions():
    """Show the React question library with answers hidden by default."""
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=REACT_QUESTIONS,
                           library_title='100 common React interview questions',
                           library_label='REACT STUDY LIBRARY', feedback_topic='react')


@app.route('/html-interview-questions')
def html_interview_questions():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=HTML_QUESTIONS,
                           library_title='100 common HTML interview questions',
                           library_label='HTML STUDY LIBRARY', feedback_topic='html')


@app.route('/css-interview-questions')
def css_interview_questions():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=CSS_QUESTIONS,
                           library_title='100 common CSS interview questions',
                           library_label='CSS STUDY LIBRARY', feedback_topic='css')


@app.route('/javascript-interview-questions')
def javascript_interview_questions():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=JAVASCRIPT_QUESTIONS,
                           library_title='100 common JavaScript interview questions',
                           library_label='JAVASCRIPT STUDY LIBRARY', feedback_topic='javascript')


@app.route('/data-science-interview-questions')
def data_science_interview_questions():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=DATA_SCIENCE_QUESTIONS,
                           library_title='100 common Data Science interview questions',
                           library_label='DATA SCIENCE STUDY LIBRARY', feedback_topic='data-science')


@app.route('/feedback-practice/<topic>', methods=['GET', 'POST'])
def feedback_practice(topic):
    """Answer ten library prompts and save each response to practice history."""
    if not login_required():
        return redirect(url_for('login'))

    topic_data = FEEDBACK_TOPICS.get(topic)
    if topic_data is None:
        abort(404)
    category, library = topic_data
    questions = library[:10]
    form = FeedbackPracticeForm()

    if form.validate_on_submit():
        answers = [request.form.get('answer_{}'.format(index), '').strip()
                   for index in range(len(questions))]
        if any(len(answer) < 30 for answer in answers):
            flash('Please write at least 30 characters for every answer.', 'warning')
        else:
            saved_questions = []
            for prompt, unused_answer in questions:
                question = Question.query.filter_by(category=category, text=prompt).first()
                if question is None:
                    question = Question(category=category, difficulty='Practice', text=prompt)
                    db.session.add(question)
                saved_questions.append(question)
            db.session.flush()

            for question, answer in zip(saved_questions, answers):
                score, feedback, unused_source = fallback_feedback(answer)
                db.session.add(Attempt(
                    user_id=g.user.id, question_id=question.id, answer=answer,
                    score=score, feedback=feedback, feedback_source='feedback practice'
                ))
            db.session.commit()
            flash('Saved 10 {} feedback-practice answers to your history.'.format(category), 'success')
            return redirect(url_for('dashboard'))

    return render_template('feedback_practice.html', form=form, topic=topic,
                           category=category, questions=questions)


@app.route('/practice')
def practice():
    if not login_required():
        return redirect(url_for('login'))
    category = request.args.get('category')
    query = Question.query.filter_by(category=category) if category else Question.query
    question = query.order_by(func.random()).first()
    if question is None:
        flash('Run seed.py to add starter questions.', 'warning')
        return redirect(url_for('dashboard'))
    return render_template('practice.html', question=question, form=AnswerForm())


@app.post('/practice/<int:question_id>')
def submit_answer(question_id):
    if not login_required():
        return redirect(url_for('login'))
    question = db.session.get(Question, question_id)
    if question is None:
        abort(404)
    form = AnswerForm()
    if not form.validate_on_submit():
        return render_template('practice.html', question=question, form=form), 400
    score, feedback, source = get_feedback(question, form.answer.data)
    attempt = Attempt(user_id=g.user.id, question_id=question.id,
                      answer=form.answer.data, score=score,
                      feedback=feedback, feedback_source=source)
    db.session.add(attempt)
    db.session.commit()
    return redirect(url_for('attempt_detail', attempt_id=attempt.id))


@app.route('/attempts/<int:attempt_id>')
def attempt_detail(attempt_id):
    if not login_required():
        return redirect(url_for('login'))
    attempt = db.session.get(Attempt, attempt_id)
    if attempt is None:
        abort(404)
    if attempt.user_id != g.user.id:
        abort(403)
    return render_template('feedback.html', attempt=attempt,
                           delete_form=DeleteAttemptForm())


@app.post('/attempts/<int:attempt_id>/delete')
def delete_attempt(attempt_id):
    """Delete only an attempt belonging to the signed-in user."""
    if not login_required():
        return redirect(url_for('login'))
    form = DeleteAttemptForm()
    if not form.validate_on_submit():
        abort(400)
    attempt = db.session.get(Attempt, attempt_id)
    if attempt is None:
        abort(404)
    if attempt.user_id != g.user.id:
        abort(403)
    db.session.delete(attempt)
    db.session.commit()
    flash('Practice answer deleted. You can now retry the question.', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

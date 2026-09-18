"""Interview Coach: a small Flask app for interview practice."""

import json
import os
import secrets

from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy import func

from forms import (AnswerForm, ChatForm, DeleteAttemptForm, FeedbackPracticeForm,
                   GuestLoginForm, LoginForm, SignupForm)
from models import Attempt, Question, User, db
from python_questions import PYTHON_QUESTIONS
from sql_questions import SQL_QUESTIONS
from behavioral_questions import BEHAVIORAL_QUESTIONS
from react_questions import REACT_QUESTIONS
from typescript_questions import TYPESCRIPT_QUESTIONS
from web_questions import CSS_QUESTIONS, HTML_QUESTIONS, JAVASCRIPT_QUESTIONS
from data_science_questions import DATA_SCIENCE_QUESTIONS
from ai_ml_questions import AI_ML_QUESTIONS
from mini_projects import MINI_PROJECTS, language_projects
from mini_project_preview import create_python_preview, python_response, javascript_response
from coding_patterns import CODING_PATTERNS
from language_comparison import COMPARISONS, OPERATIONS, DSA_PATTERNS
from full_stack_questions import FULL_STACK_QUESTIONS
from frontend_questions import FRONTEND_QUESTIONS
from backend_questions import BACKEND_QUESTIONS
from python_tricky_questions import PYTHON_TRICKY_QUESTIONS
from javascript_tricky_questions import JAVASCRIPT_TRICKY_QUESTIONS

CURR_USER_KEY = 'current_user_id'
FEEDBACK_TOPICS = {
    'python': ('Python', PYTHON_QUESTIONS),
    'sql': ('SQL', SQL_QUESTIONS),
    'behavioral': ('Behavioral', BEHAVIORAL_QUESTIONS),
    'react': ('React', REACT_QUESTIONS),
    'html': ('HTML', HTML_QUESTIONS),
    'css': ('CSS', CSS_QUESTIONS),
    'javascript': ('JavaScript', JAVASCRIPT_QUESTIONS),
    'typescript': ('TypeScript', TYPESCRIPT_QUESTIONS),
    'data-science': ('Data Science', DATA_SCIENCE_QUESTIONS),
    'ai-ml': ('AI/Machine Learning', AI_ML_QUESTIONS),
    'full-stack': ('Full Stack Developer', FULL_STACK_QUESTIONS),
    'frontend': ('Frontend Developer', FRONTEND_QUESTIONS),
    'backend': ('Backend Developer', BACKEND_QUESTIONS),
    'python-tricky': ('Python Tricky Questions', PYTHON_TRICKY_QUESTIONS),
    'javascript-tricky': ('JavaScript Tricky Questions', JAVASCRIPT_TRICKY_QUESTIONS),
}

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'change-me-before-deploying'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'postgresql+psycopg:///interview_coach'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db.init_app(app)
python_todo_preview = create_python_preview(app.config['SECRET_KEY'])
python_table_demo = create_python_preview(app.config['SECRET_KEY'], tables=True)


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


def chat_answer(messages):
    """Answer interview questions with OpenAI; the key remains server-side."""
    if not os.environ.get('OPENAI_API_KEY'):
        return ('Add `OPENAI_API_KEY` to your environment to enable AI chat. '
                'This local app cannot generate a full answer without the key.')
    try:
        from openai import (APIConnectionError, APIStatusError, AuthenticationError,
                            OpenAI, RateLimitError)
        response = OpenAI().responses.create(
            model=os.environ.get('OPENAI_MODEL', 'gpt-5'),
            instructions=('You are Interview Coach, a concise and encouraging coach for coding and interview questions. '
                          'Explain clearly, give a short example when helpful, and identify important interview talking points.'),
            input=[{'role': item['role'], 'content': item['content']} for item in messages[-10:]],
            max_output_tokens=700,
            store=False,
        )
        return response.output_text
    except AuthenticationError:
        app.logger.warning('OpenAI chat authentication failed.')
        return 'OpenAI rejected the API key. Create a new key, export it in the Flask terminal, then restart Flask.'
    except RateLimitError:
        app.logger.warning('OpenAI chat rate limit or billing limit reached.')
        return 'OpenAI rate limit or billing limit reached. Check your OpenAI project billing and try again shortly.'
    except APIConnectionError:
        app.logger.warning('OpenAI chat connection failed.')
        return 'Could not connect to OpenAI. Check your internet connection and try again.'
    except APIStatusError as error:
        app.logger.warning('OpenAI chat request failed with status %s.', error.status_code)
        return 'OpenAI could not process this request (HTTP {}). Check OPENAI_MODEL and your project access.'.format(error.status_code)
    except Exception as error:
        app.logger.exception('Unexpected OpenAI chat error.')
        return ('The AI coach encountered a {}. Check the Flask terminal for the full error, '
                'then try again.').format(type(error).__name__)
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
    categories = list(dict.fromkeys(['Python', 'Python Tricky Questions', 'SQL', 'Behavioral', 'React', 'HTML', 'CSS', 'JavaScript', 'JavaScript Tricky Questions', 'TypeScript', 'Data Science', 'AI/Machine Learning', 'Full Stack Developer', 'Frontend Developer', 'Backend Developer'] + database_categories))
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


@app.route('/mini-projects/python/preview/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/mini-projects/python/preview/<path:path>', methods=['GET', 'POST'])
def python_project_preview(path):
    if not login_required():
        return redirect(url_for('login'))
    return python_response(python_todo_preview, path)


@app.route('/mini-projects/javascript/preview/', defaults={'filename': 'index.html'})
@app.route('/mini-projects/javascript/preview/<filename>')
def javascript_project_preview(filename):
    if not login_required():
        return redirect(url_for('login'))
    return javascript_response(filename)


@app.route('/mini-projects/react/preview/')
def react_project_preview():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('react_preview.html')


@app.route('/mini-projects/python/tables/preview/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/mini-projects/python/tables/preview/<path:path>', methods=['GET', 'POST'])
def python_table_preview(path):
    if not login_required():
        return redirect(url_for('login'))
    return python_response(python_table_demo, path)


@app.route('/mini-projects/javascript/tables/preview/', defaults={'filename': 'index.html'})
@app.route('/mini-projects/javascript/tables/preview/<filename>')
def javascript_table_preview(filename):
    if not login_required():
        return redirect(url_for('login'))
    return javascript_response(filename, tables=True)


@app.route('/mini-projects/react/tables/preview/')
def react_table_preview():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('react_preview.html', tables=True)


@app.route('/mini-projects/<language>')
def mini_project(language):
    if not login_required():
        return redirect(url_for('login'))
    project = MINI_PROJECTS.get(language)
    if project is None:
        abort(404)
    return render_template('mini_project.html', project=project, language=language,
                           projects=MINI_PROJECTS, entries=language_projects(language))


@app.route('/coding-patterns')
def coding_patterns():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('coding_patterns.html', patterns=CODING_PATTERNS)


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    """Session-based interview chat retaining the latest six exchanges."""
    if not login_required():
        return redirect(url_for('login'))
    form = ChatForm()
    messages = session.get('chat_messages', [])
    if form.validate_on_submit():
        messages.append({'role': 'user', 'content': form.message.data.strip()})
        messages.append({'role': 'assistant', 'content': chat_answer(messages)})
        session['chat_messages'] = messages[-12:]
        session.modified = True
        return redirect(url_for('chat'))
    return render_template('chat.html', form=form, messages=messages)


@app.post('/chat/clear')
def clear_chat():
    if not login_required():
        return redirect(url_for('login'))
    session.pop('chat_messages', None)
    return redirect(url_for('chat'))


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


@app.route('/python-vs-javascript')
def language_comparison():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('language_comparison.html', comparisons=COMPARISONS,
                           operations=OPERATIONS, patterns=DSA_PATTERNS)


@app.route('/typescript-interview-questions')
def typescript_interview_questions():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=TYPESCRIPT_QUESTIONS,
                           library_title='100 common TypeScript interview questions',
                           library_label='TYPESCRIPT STUDY LIBRARY', feedback_topic='typescript')


@app.route('/data-science-interview-questions')
def data_science_interview_questions():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=DATA_SCIENCE_QUESTIONS,
                           library_title='100 common Data Science interview questions',
                           library_label='DATA SCIENCE STUDY LIBRARY', feedback_topic='data-science')


@app.route('/ai-ml-interview-questions')
def ai_ml_interview_questions():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=AI_ML_QUESTIONS,
                           library_title='100 common AI/Machine Learning interview questions',
                           library_label='AI/MACHINE LEARNING STUDY LIBRARY', feedback_topic='ai-ml')


@app.route('/full-stack-interview-questions')
def full_stack_interview_questions():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=FULL_STACK_QUESTIONS,
                           library_title='100 common Full Stack Developer interview questions',
                           library_label='FULL STACK STUDY LIBRARY', feedback_topic='full-stack')


@app.route('/frontend-interview-questions')
def frontend_interview_questions():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=FRONTEND_QUESTIONS,
                           library_title='100 common Frontend Developer interview questions',
                           library_label='FRONTEND STUDY LIBRARY', feedback_topic='frontend')


@app.route('/backend-interview-questions')
def backend_interview_questions():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=BACKEND_QUESTIONS,
                           library_title='100 common Backend Developer interview questions',
                           library_label='BACKEND STUDY LIBRARY', feedback_topic='backend')


@app.route('/python-tricky-interview-questions')
def python_tricky_interview_questions():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=PYTHON_TRICKY_QUESTIONS,
                           library_title='100 tricky Python coding challenges',
                           library_label='PYTHON TRICKY QUESTIONS', feedback_topic='python-tricky')


@app.route('/javascript-tricky-interview-questions')
def javascript_tricky_interview_questions():
    if not login_required():
        return redirect(url_for('login'))
    return render_template('python_questions.html', questions=JAVASCRIPT_TRICKY_QUESTIONS,
                           library_title='100 tricky JavaScript coding challenges',
                           library_label='JAVASCRIPT TRICKY QUESTIONS', feedback_topic='javascript-tricky')


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

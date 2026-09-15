"""Create the database and add starter interview questions. Run: python3 seed.py"""

from app import app
from models import Question, db

QUESTIONS = [
    ('Python', 'Beginner', 'What is the difference between a list and a tuple in Python? When would you use each?'),
    ('Python', 'Intermediate', 'What is a generator in Python, and why can it be more memory efficient than a list?'),
    ('SQL', 'Beginner', 'How would you find customers who have never placed an order? Explain the join you would use.'),
    ('SQL', 'Intermediate', 'What is an index in a database? Describe one benefit and one tradeoff.'),
    ('Behavioral', 'Beginner', 'Tell me about a time you received difficult feedback. What did you do?'),
    ('Behavioral', 'Intermediate', 'Tell me about a project that did not go as planned. How did you respond?'),
]

with app.app_context():
    db.create_all()
    for category, difficulty, text in QUESTIONS:
        if not Question.query.filter_by(text=text).first():
            db.session.add(Question(category=category, difficulty=difficulty, text=text))
    db.session.commit()
    print('Database ready. Starter questions are available.')

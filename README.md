# Interview Coach

A Flask app for practicing technical and behavioral interview answers.

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="a-long-random-secret"
python3 seed.py
flask --app app run --debug
```

Open http://127.0.0.1:5000, create an account, and choose a practice category.

## Optional AI feedback

The app works without an API key and gives local rules-based feedback. To enable
OpenAI feedback, set these before starting Flask:

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_MODEL="gpt-5"
```

Keep API keys on the server. Never put them in templates, JavaScript, or Git.

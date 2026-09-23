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

### Developer footer

The shared footer displays your public profile on all main app pages. Set these
optional environment variables before starting the app (restart after changing):

- `PROFILE_NAME`: your display name
- `PROFILE_LOCATION`: your location
- `PROFILE_BIO`: your short introduction
- `PROFILE_EMAIL`: your email address
- `PROFILE_GITHUB`: full HTTPS GitHub profile URL
- `PROFILE_LINKEDIN`: full HTTPS LinkedIn profile URL
- `PROFILE_X`: full HTTPS X profile URL

The footer defaults to Sanam Maharjan’s contact details in `developer_profile.py`.
Environment variables override those defaults; setting a contact value to an empty
string hides that link.

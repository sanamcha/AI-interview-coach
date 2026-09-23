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

### Render database setup

Set `DATABASE_URL` in the Render service's Environment settings to the Neon
PostgreSQL connection string, keeping its `sslmode=require` and other query
parameters. The app accepts `postgresql://`, `postgres://`, or
`postgresql+psycopg://` and uses the installed psycopg 3 driver. Set a random
`SECRET_KEY` as well. Local `.env.local` and `.neon` files are not uploaded to
Render and do not configure the hosted service.

Build command: `pip install -r requirements.txt`

Start command: `python seed.py && gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120`

The seed script creates missing tables and starter questions without deleting
existing data. For an existing schema requiring changes, use a reviewed migration.
If deployment fails, inspect the database error immediately above SQLAlchemy's
error-help link; the link alone does not identify the cause.

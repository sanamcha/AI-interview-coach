"""Normalize database configuration without exposing connection credentials."""
import os


def database_url():
    value = os.environ.get('DATABASE_URL', '').strip()
    if not value:
        if os.environ.get('RENDER'):
            raise RuntimeError(
                'DATABASE_URL is missing. Add your Neon PostgreSQL connection '
                'string in Render Environment settings, then redeploy.'
            )
        return 'postgresql+psycopg:///interview_coach'
    # Neon supplies a standard PostgreSQL URL; this project uses psycopg 3.
    for prefix in ('postgres://', 'postgresql://'):
        if value.startswith(prefix):
            return 'postgresql+psycopg://' + value[len(prefix):]
    return value

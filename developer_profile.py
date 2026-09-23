"""Public portfolio details. Set these environment variables before starting Flask."""
import os

PROFILE = {
    'name': os.environ.get('PROFILE_NAME', 'Sanam Maharjan'),
    'location': os.environ.get('PROFILE_LOCATION', 'San Francisco Bay Area, CA'),
    'headline': 'Open to full-stack developer roles',
    'bio': os.environ.get('PROFILE_BIO', 'I built Interview Coach to share interview preparation and hands-on coding projects. I’m looking for opportunities to contribute as a full-stack developer.'),
    'email': os.environ.get('PROFILE_EMAIL', 'mhr.sanam@gmail.com'),
    'github': os.environ.get('PROFILE_GITHUB', 'https://github.com/sanamcha'),
    'linkedin': os.environ.get('PROFILE_LINKEDIN', 'https://linkedin.com/in/sanam-maharjan'),
    'x': os.environ.get('PROFILE_X', 'https://x.com/san_mhr'),
}

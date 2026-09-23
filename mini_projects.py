"""Mini-project catalog; source files are shared by the examples and study pages."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent / 'project_examples'
MINI_PROJECTS = {
    'python': {
        'language': 'Python',
        'stack': 'Python · Flask · HTML · CSS',
        'summary': 'Build a server-rendered To-Do List with forms, routes, validation, and a separate task list for each browser session.',
        'setup': 'Create a new folder and save the files below using the shown paths. Install Python 3.10+ first. Run these commands from that folder:',
        'commands': 'python3 -m venv .venv\nsource .venv/bin/activate\n# Windows: .venv\\Scripts\\activate\npython -m pip install -r requirements.txt\npython app.py',
        'open': 'Open http://127.0.0.1:5001 in your browser.',
        'storage': 'Tasks are stored in a signed session cookie, with a 10-task limit for this small demo. They survive reloads in the same session. Restarting the server resets its signing key unless you set a stable SECRET_KEY environment variable. Use a database for a larger app.',
        'steps': ['GET / renders the current session tasks with a Jinja template.', 'POST / trims and validates input, adds a task, and redirects to avoid duplicate form submission on refresh.', 'Toggle and delete routes update tasks by ID; CSRF tokens protect all POST forms.', 'The stylesheet gives the HTML a responsive layout and marks completed tasks.'],
        'files': ['requirements.txt', 'app.py', 'templates/index.html', 'static/style.css'],
    },
    'javascript': {
        'language': 'JavaScript',
        'stack': 'JavaScript · HTML · CSS',
        'summary': 'Build a browser-based To-Do List using arrays, DOM creation, and event listeners. No framework or build tool is required.',
        'setup': 'Create a folder and save all three files below together. Open index.html directly, or serve the folder with this optional command if Python is installed:',
        'commands': 'python3 -m http.server 8000',
        'open': 'For the optional server, open http://localhost:8000.',
        'storage': 'Tasks live in memory and reset when the page reloads. Add localStorage as a follow-up exercise.',
        'steps': ['A submit listener prevents a page reload and rejects blank or whitespace-only tasks.', 'Each task gets a stable ID, text, and completion flag.', 'render() builds DOM elements; textContent displays task text without interpreting HTML.', 'Checkboxes toggle completion and Delete filters the selected ID out of the array.'],
        'files': ['index.html', 'app.js', 'style.css'],
    },
    'react': {
        'language': 'React',
        'stack': 'React · JavaScript (JSX) · HTML · CSS · Vite',
        'summary': 'Build the same To-Do List with a controlled input, component state, stable keys, and immutable updates.',
        'setup': 'Install a supported Node.js version (22.12+ or newer supported LTS) and npm. Create a Vite React project with these commands, then replace src/App.jsx, src/App.css, and src/index.css with the files below. Keep Vite’s generated index.html and src/main.jsx.',
        'commands': 'npm create vite@latest todo-react -- --template react\ncd todo-react\nnpm install\n# Replace the three source files below, then start:\nnpm run dev',
        'open': 'Open the local URL printed by Vite (usually http://localhost:5173).',
        'storage': 'Tasks are held in React state and reset on reload. Adding persistence is an optional extension.',
        'steps': ['useState stores tasks and the controlled input value; useRef tracks the next task ID.', 'Submitting creates a task and appends it with a new array.', 'map updates the selected task and filter deletes it, without mutating the previous state.', 'React renders the task list from state and uses stable task IDs as keys.'],
        'files': ['src/App.jsx', 'src/App.css', 'src/index.css'],
    },
}


def project_files(language, tables=False):
    """Read only catalog-approved files, never an arbitrary requested path."""
    return [(name, (PROJECT_ROOT / (language + ('_tables' if tables else '')) / name).read_text())
            for name in MINI_PROJECTS[language]['files']]


def language_projects(language):
    base = MINI_PROJECTS[language]
    return [dict(base, title='To-Do List', files=project_files(language),
                 preview_endpoint=language + '_project_preview'),
            dict(base, title='To-Do List Tables', files=project_files(language, tables=True),
                 summary='Build a To-Do List as a table with numbered rows, task titles, status, and action buttons.',
                 steps=base['steps'] + ['Render tasks in a semantic table with column headers and an empty-state row. Row numbers follow the current order; stable task IDs identify actions.'],
                 preview_endpoint=language + '_table_preview'), api_project(language), rating_project(language), pagination_project(language), survey_project(language), quiz_project(language), chat_project(language)]


def api_project(language):
    base = MINI_PROJECTS[language]
    names = {'python': ['requirements.txt', 'app.py', 'templates/index.html', 'static/app.js', 'static/style.css'],
             'javascript': ['index.html', 'app.js', 'style.css'],
             'react': ['src/App.jsx', 'src/App.css', 'src/index.css']}[language]
    return dict(base, title='API CRUD', is_api=True,
                summary='Load 20 posts from an API, then add, edit, and delete items in a table.',
                storage='JSONPlaceholder simulates writes: changes are kept in this page until reload, not persisted on the API. Each created row has a unique local key because the API can return the same ID repeatedly.',
                steps=['GET /posts?_limit=20 fetches the initial 20 items.',
                       'POST /posts adds a title. PATCH /posts/:id edits it. DELETE /posts/:id removes it.',
                       'Python makes upstream requests on the server; JavaScript and React use browser fetch.',
                       'Only update the table after a successful request; show loading and retryable error messages.'],
                files=[(name, (PROJECT_ROOT / (language + '_api') / name).read_text()) for name in names],
                preview_endpoint=language + '_api_preview')


def rating_project(language):
    base = MINI_PROJECTS[language]
    names = base['files']
    return dict(base, title='5-Star Ratings', is_rating=True,
                summary='Select one to five stars in gold; click the selected rating again to reset all stars to grey.',
                storage='The Python rating stays in this browser session. JavaScript and React ratings reset on reload.',
                commands=base['commands'].replace('todo-react', 'star-rating-react'),
                steps=['Start with a rating of zero and five grey star buttons.',
                       'Clicking a star sets its value as the rating. Clicking the same rating again resets it to zero.',
                       'Stars at or below the rating turn gold; the remaining stars stay grey.',
                       {'python': 'Flask validates a CSRF-protected form, updates the session, and renders the new rating.',
                        'javascript': 'Click listeners update the rating and toggle the selected CSS class.',
                        'react': 'useState stores the rating; React derives star colors from state.'}[language],
                       'Button labels, pressed state, visible focus, and text feedback make the control keyboard accessible.'],
                files=[(name, (PROJECT_ROOT / (language + '_rating') / name).read_text()) for name in names],
                preview_endpoint=language + '_rating_preview')


def pagination_project(language):
    base = MINI_PROJECTS[language]
    return dict(base, title='Pagination', is_pagination=True,
                summary='Browse 20 fruit names, five per page, using Previous and Next arrow buttons.',
                storage='Python keeps the page number in the URL, so refreshing retains the page. JavaScript and React reset to page one on reload. No API or database is needed.',
                commands=base['commands'].replace('todo-react', 'pagination-react'),
                steps=['Create a list of 20 fruits and set the page size to five: four pages in total.',
                       'Calculate start = (page - 1) * pageSize and slice five items from that offset.',
                       'Previous and Next decrease or increase the page number within the valid range.',
                       'Disable Previous on the first page and Next on the last page.',
                       {'python': 'Flask reads and validates the page query parameter, then renders the selected slice.',
                        'javascript': 'Click handlers change the page and render its slice in the DOM.',
                        'react': 'useState tracks the page; derive the visible slice directly from that state.'}[language]],
                files=[(name, (PROJECT_ROOT / (language + '_pagination') / name).read_text()) for name in base['files']],
                preview_endpoint=language + '_pagination_preview')


def survey_project(language):
    base = MINI_PROJECTS[language]
    names = base['files'] + (['templates/results.html'] if language == 'python' else [])
    return dict(base, title='Survey App', is_survey=True,
                summary='Answer three randomly selected questions, one per page: two Yes/No choices and a final text answer.',
                storage='Questions are selected once per survey. Back to Survey preserves your answers; New random survey starts over. Python stores the survey in the browser session. JavaScript and React reset on reload.',
                commands=base['commands'].replace('todo-react', 'survey-react'),
                steps=['Randomly pick two distinct Yes/No questions and one text question.',
                       'Show one question at a time and require an answer before moving on.',
                       'Submit the third answer to a separate results view listing every question and answer.',
                       'Back to Survey lets you review and edit the same survey. New random survey clears answers and picks again.',
                       {'python': 'Flask uses session state, validated CSRF-protected forms, and a /results route.',
                        'javascript': 'DOM events collect answers and hash navigation switches between questions and results.',
                        'react': 'React state holds questions and answers; hash navigation selects the current page.'}[language]],
                files=[(name, (PROJECT_ROOT / (language + '_survey') / name).read_text()) for name in names],
                preview_endpoint=language + '_survey_preview')


def quiz_project(language):
    base = MINI_PROJECTS[language]
    names = base['files'] + (['templates/results.html'] if language == 'python' else [])
    return dict(base, title='Quiz App', is_quiz=True,
                summary='Answer five random multiple-choice questions, one per page, then see your score and percentage.',
                storage='Five distinct questions are chosen once per attempt. Python retains progress in this browser session. JavaScript and React reset on reload. Try a new quiz clears the attempt and picks again.',
                commands=base['commands'].replace('todo-react', 'quiz-react'),
                steps=['Select five questions without replacement from a bank of ten.',
                       'Require one answer per question before advancing. Keep the selected questions fixed throughout the attempt.',
                       'Compare each submitted answer with its correct choice and count the matches.',
                       'Calculate percentage = correct answers / 5 × 100 and show an answer review.',
                       'Try a new quiz resets progress and samples five questions again.'],
                files=[(name, (PROJECT_ROOT / (language + '_quiz') / name).read_text()) for name in names],
                preview_endpoint=language + '_quiz_preview')


def chat_project(language):
    base = MINI_PROJECTS[language]
    names = (['server.py', 'requirements.txt', 'vite.config.js', 'src/App.jsx', 'src/App.css', 'src/index.css'] if language == 'react'
             else ['requirements.txt', 'app.py', 'templates/index.html', 'static/app.js', 'static/style.css'])
    setup = 'Save the files below in a new folder. Python handles shared message storage; JavaScript handles the browser interface. Install Python 3.10+ and run:'
    commands = MINI_PROJECTS['python']['commands']
    if language == 'react':
        setup = 'Create a Vite React project, then save the files below in it. Install Python 3.10+ and a supported Node.js version. Run the API in one terminal and Vite in another:'
        commands = 'npm create vite@latest chat-react -- --template react\ncd chat-react\nnpm install\n# Save the files below, then in terminal 1:\npython3 -m venv .venv\nsource .venv/bin/activate\n# Windows: .venv\\Scripts\\activate\npip install -r requirements.txt\npython server.py\n# In terminal 2, from chat-react:\nnpm run dev'
    return dict(base, title='Chat App', is_chat=True, setup=setup, commands=commands,
                open='Open the Vite URL in two tabs.' if language == 'react' else 'Open http://127.0.0.1:5001 in two tabs.',
                summary='Send and receive messages between named participants in the same room.',
                storage='All live previews share a Flask API and SQLite history. Names are display labels, not verified accounts. Room names separate conversations but are not private access controls. The newest 100 messages per room are retained. Standalone projects share messages when connected to the same server.',
                steps=['Join with a display name and room name. Open another tab with a different name and the same room.',
                       'POST sends a validated message to the Flask API, which saves it in SQLite.',
                       'GET polls the room every 1.5 seconds to display messages from all participants.',
                       'Render messages as text, show request errors, and stop polling when leaving.',
                       'JavaScript uses DOM events; React uses state and an effect with polling cleanup. Python supplies the shared backend.'],
                files=[(name, (PROJECT_ROOT / (language + '_chat') / name).read_text()) for name in names],
                preview_endpoint=language + '_chat_preview')

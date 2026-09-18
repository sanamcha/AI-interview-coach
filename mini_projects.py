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


def project_files(language):
    """Read only catalog-approved files, never an arbitrary requested path."""
    return [(name, (PROJECT_ROOT / language / name).read_text())
            for name in MINI_PROJECTS[language]['files']]

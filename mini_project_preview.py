"""Serve runnable tutorial previews without sharing the coach's session cookie."""
import importlib.util
import sys

from flask import Response, request, send_from_directory
from mini_projects import PROJECT_ROOT


def create_python_preview(secret_key, tables=False):
    folder = "python_tables" if tables else "python"
    module_name = "python_table_preview" if tables else "python_todo_preview"
    spec = importlib.util.spec_from_file_location(module_name, PROJECT_ROOT / folder / 'app.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    demo = module.app
    demo.config.update(
        SECRET_KEY=secret_key,
        SESSION_COOKIE_NAME=module_name,
        SESSION_COOKIE_PATH='/mini-projects/python/' + ('tables/preview' if tables else 'preview'),
    )
    return demo


def python_response(demo, path):
    environ = request.environ.copy()
    environ['SCRIPT_NAME'] = request.script_root + demo.config['SESSION_COOKIE_PATH']
    environ['PATH_INFO'] = '/' + path
    return Response.from_app(demo.wsgi_app, environ)


def javascript_response(filename, tables=False):
    if filename not in ('index.html', 'app.js', 'style.css'):
        from flask import abort
        abort(404)
    return send_from_directory(PROJECT_ROOT / ('javascript_tables' if tables else 'javascript'), filename)

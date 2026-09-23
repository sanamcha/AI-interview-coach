"""Serve runnable tutorial previews without sharing the coach's session cookie."""
import importlib.util
import sys

from flask import Response, request, send_from_directory
from mini_projects import PROJECT_ROOT


def create_python_preview(secret_key, tables=False, api=False, rating=False, pagination=False, survey=False, quiz=False, chat=False):
    folder = "python_chat" if chat else "python_quiz" if quiz else "python_survey" if survey else "python_pagination" if pagination else "python_rating" if rating else "python_api" if api else "python_tables" if tables else "python"
    module_name = "python_chat_preview" if chat else "python_quiz_preview" if quiz else "python_survey_preview" if survey else "python_pagination_preview" if pagination else "python_rating_preview" if rating else "python_api_preview" if api else "python_table_preview" if tables else "python_todo_preview"
    spec = importlib.util.spec_from_file_location(module_name, PROJECT_ROOT / folder / 'app.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    demo = module.app
    demo.config.update(
        SECRET_KEY=secret_key,
        SESSION_COOKIE_NAME=module_name,
        SESSION_COOKIE_PATH='/mini-projects/python/' + ('chat/preview' if chat else 'quiz/preview' if quiz else 'survey/preview' if survey else 'pagination/preview' if pagination else 'rating/preview' if rating else 'api/preview' if api else 'tables/preview' if tables else 'preview'),
    )
    return demo


def python_response(demo, path):
    environ = request.environ.copy()
    environ['SCRIPT_NAME'] = request.script_root + demo.config['SESSION_COOKIE_PATH']
    environ['PATH_INFO'] = '/' + path
    return Response.from_app(demo.wsgi_app, environ)


def javascript_response(filename, tables=False, api=False, rating=False, pagination=False, survey=False, quiz=False, chat=False):
    if filename not in ('index.html', 'app.js', 'style.css'):
        from flask import abort
        abort(404)
    return send_from_directory(PROJECT_ROOT / ('javascript_quiz' if quiz else 'javascript_survey' if survey else 'javascript_pagination' if pagination else 'javascript_rating' if rating else 'javascript_api' if api else 'javascript_tables' if tables else 'javascript'), filename)

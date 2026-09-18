"""Build code-first libraries while retaining the application's (prompt, answer) API."""


def build_coding_library(language, cases):
    questions = []
    for title, code, result, task, solution, checks, variation, variation_answer in cases:
        context = f'{title} ({language})\n\n{code}'
        questions.extend([
            (f'Predict the output or exception and explain the execution.\n\n{context}', result),
            (f'Debug / implement: {task}\n\n{context}', solution),
            (f'Write regression tests for this change: {task}\nInclude the expected results.\n\n{context}', checks),
            (f'Trace the changed code: {variation}\n\n{context}', variation_answer),
        ])
    return questions

import math
from flask import Flask, render_template, request
app = Flask(__name__)

def calculate(left, operation, right):
    if not left.strip() or not right.strip():
        raise ValueError('Enter both numbers.')
    try:
        a, b = float(left), float(right)
    except ValueError:
        raise ValueError('Enter valid numbers.')
    if not math.isfinite(a) or not math.isfinite(b):
        raise ValueError('Enter finite numbers.')
    if operation == 'add':
        result = a + b
    elif operation == 'subtract':
        result = a - b
    elif operation == 'multiply':
        result = a * b
    elif operation == 'divide':
        if b == 0:
            raise ValueError('Cannot divide by zero.')
        result = a / b
    else:
        raise ValueError('Choose a valid operation.')
    if not math.isfinite(result):
        raise ValueError('Result is too large. Try smaller numbers.')
    return format(result if result != 0 else 0, '.12g')

@app.get('/')
def index():
    left = request.args.get('left', '')
    right = request.args.get('right', '')
    operation = request.args.get('operation', 'add')
    result = 'Enter two numbers to begin.'
    if request.args:
        try:
            result = 'Result: ' + calculate(left, operation, right)
        except ValueError as error:
            result = str(error)
    return render_template('index.html', left=left, right=right, operation=operation, result=result)

if __name__ == '__main__':
    app.run(port=5001)

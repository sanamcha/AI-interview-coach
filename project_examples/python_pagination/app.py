"""Server-rendered pagination: page number is carried in the URL."""
from flask import Flask, render_template, request
app = Flask(__name__)
ITEMS = ['Apple', 'Banana', 'Orange', 'Mango', 'Grape', 'Pineapple', 'Strawberry', 'Blueberry', 'Raspberry', 'Watermelon', 'Peach', 'Pear', 'Plum', 'Kiwi', 'Cherry', 'Lemon', 'Lime', 'Papaya', 'Apricot', 'Guava']
PAGE_SIZE = 5

@app.get('/')
def index():
    total_pages = (len(ITEMS) + PAGE_SIZE - 1) // PAGE_SIZE
    page = request.args.get('page', default=1, type=int)
    page = max(1, min(page, total_pages))
    start = (page - 1) * PAGE_SIZE
    return render_template('index.html', items=ITEMS[start:start + PAGE_SIZE],
                           page=page, total_pages=total_pages, start=start,
                           end=min(start + PAGE_SIZE, len(ITEMS)), total=len(ITEMS))

if __name__ == '__main__':
    app.run(port=5001)

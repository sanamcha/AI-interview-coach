const items = ["Apple", "Banana", "Orange", "Mango", "Grape", "Pineapple", "Strawberry", "Blueberry", "Raspberry", "Watermelon", "Peach", "Pear", "Plum", "Kiwi", "Cherry", "Lemon", "Lime", "Papaya", "Apricot", "Guava"];
const pageSize = 5;
const totalPages = Math.ceil(items.length / pageSize);
let page = 1;
const list = document.querySelector('#items');
const previous = document.querySelector('#previous');
const next = document.querySelector('#next');
const status = document.querySelector('#status');
function render() {
  const start = (page - 1) * pageSize;
  list.replaceChildren();
  list.start = start + 1;
  for (const fruit of items.slice(start, start + pageSize)) {
    const row = document.createElement('li');
    row.textContent = fruit;
    list.append(row);
  }
  status.textContent = `Page ${page} of ${totalPages} · ${start + 1}–${Math.min(start + pageSize, items.length)} of ${items.length}`;
  previous.disabled = page === 1;
  next.disabled = page === totalPages;
}
previous.addEventListener('click', () => { page = Math.max(1, page - 1); render(); });
next.addEventListener('click', () => { page = Math.min(totalPages, page + 1); render(); });
render();

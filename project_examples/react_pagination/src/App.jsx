import {useState} from 'react';
import './App.css';
const items = ["Apple", "Banana", "Orange", "Mango", "Grape", "Pineapple", "Strawberry", "Blueberry", "Raspberry", "Watermelon", "Peach", "Pear", "Plum", "Kiwi", "Cherry", "Lemon", "Lime", "Papaya", "Apricot", "Guava"];
const pageSize = 5;
const totalPages = Math.ceil(items.length / pageSize);
export default function App() {
  const [page, setPage] = useState(1);
  const start = (page - 1) * pageSize;
  return <main>
    <h1>Fruit pagination</h1><p>20 fruits · 5 items per page</p>
    <ol start={start + 1}>{items.slice(start, start + pageSize).map(fruit => <li key={fruit}>{fruit}</li>)}</ol>
    <nav className="pagination" aria-label="Fruit pages">
      <button type="button" aria-label="Previous page" title="Previous page" disabled={page === 1}
        onClick={() => setPage(current => Math.max(1, current - 1))}>←</button>
      <p role="status">Page {page} of {totalPages} · {start + 1}–{Math.min(start + pageSize, items.length)} of {items.length}</p>
      <button type="button" aria-label="Next page" title="Next page" disabled={page === totalPages}
        onClick={() => setPage(current => Math.min(totalPages, current + 1))}>→</button>
    </nav>
  </main>;
}

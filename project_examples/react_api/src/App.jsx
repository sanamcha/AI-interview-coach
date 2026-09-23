import {useEffect, useRef, useState} from 'react';
import './App.css';
const API = 'https://jsonplaceholder.typicode.com/posts';
async function api(path = '', method = 'GET', data) {
  const response = await fetch(API + path, {method,
    headers: {'Content-Type': 'application/json'},
    body: data === undefined ? undefined : JSON.stringify(data),
    signal: AbortSignal.timeout(15000)});
  if (!response.ok) throw new Error(`API returned ${response.status}`);
  return method === 'DELETE' ? null : response.json();
}
export default function App() {
  const [items, setItems] = useState([]);
  const [title, setTitle] = useState('');
  const [editing, setEditing] = useState(null);
  const [busy, setBusy] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const [status, setStatus] = useState('Loading…');
  const lock = useRef(false);
  function reset() { setTitle(''); setEditing(null); }
  async function run(action) {
    if (lock.current) return;
    lock.current = true; setBusy(true); setStatus('Working…');
    try { await action(); }
    catch (error) { setStatus(`Request failed: ${error.message}. Try again.`); }
    finally { lock.current = false; setBusy(false); }
  }
  function load() {
    return run(async () => {
      const data = await api('?_limit=20');
      if (!Array.isArray(data) || data.length !== 20 || data.some(x => !Number.isInteger(x.id) || typeof x.title !== 'string')) throw new Error('Unexpected API data');
      setItems(data.map(item => ({...item, key: crypto.randomUUID()})));
      setLoaded(true); reset(); setStatus('Loaded 20 API items.');
    });
  }
  useEffect(() => { load(); }, []);
  function save(event) {
    event.preventDefault();
    const value = title.trim();
    if (!value) { setStatus('Enter a nonempty title.'); return; }
    run(async () => {
      const item = items.find(item => item.key === editing);
      if (item) {
        await api(`/${item.id}`, 'PATCH', {title: value});
        setItems(current => current.map(row => row.key === item.key ? {...row, title: value} : row));
      } else {
        const result = await api('', 'POST', {title: value, body: '', userId: 1});
        if (!Number.isInteger(result.id)) throw new Error('Missing item ID');
        const row = {id: result.id, title: value, key: crypto.randomUUID()};
        setItems(current => [row, ...current]);
      }
      reset(); setStatus('Saved (demo API).');
    });
  }
  function remove(item) {
    run(async () => {
      await api(`/${item.id}`, 'DELETE');
      setItems(current => current.filter(row => row.key !== item.key));
      if (editing === item.key) reset();
      setStatus('Deleted (demo API).');
    });
  }
  return <main>
    <h1>API CRUD</h1>
    <p>JSONPlaceholder demo: API writes are simulated. Changes remain here until reload. Newly added items can also be edited and deleted.</p>
    <form onSubmit={save}>
      <label htmlFor="title">Item title</label>
      <input id="title" value={title} onChange={e => setTitle(e.target.value)} maxLength={120} required disabled={busy || !loaded} />
      <button disabled={busy || !loaded}>{editing ? 'Save changes' : 'Add item'}</button>
      {editing && <button type="button" disabled={busy} onClick={reset}>Cancel edit</button>}
    </form>
    <p role="status">{status}</p>
    <button disabled={busy} onClick={load}>Reload 20 API items</button>
    <div className="table-scroll"><table><caption>API items</caption>
      <thead><tr><th scope="col">#</th><th scope="col">Title</th><th scope="col">Actions</th></tr></thead>
      <tbody>{items.map((item, index) => <tr key={item.key}>
        <td>{index + 1}</td><td>{item.title}</td><td>
          <button disabled={busy} aria-label={`Edit ${item.title}`} onClick={() => {setEditing(item.key); setTitle(item.title);}}>Edit</button>{' '}
          <button disabled={busy} aria-label={`Delete ${item.title}`} onClick={() => remove(item)}>Delete</button>
        </td></tr>)}
        {!items.length && <tr><td colSpan={3}>{loaded ? 'No items. Add one above.' : 'No data loaded yet.'}</td></tr>}
      </tbody></table></div>
  </main>;
}

const API = document.querySelector('meta[name=api-url]').content;
const csrf = document.querySelector('meta[name=csrf-token]').content;
const form = document.querySelector('#editor');
const input = document.querySelector('#title');
const status = document.querySelector('#status');
const body = document.querySelector('#items');
const save = document.querySelector('#save');
const cancel = document.querySelector('#cancel');
const reload = document.querySelector('#reload');
let items = [], editing = null, busy = false, loaded = false;

async function api(path = '', method = 'GET', data) {
  const response = await fetch(API + path, {
    method, headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrf},
    body: data === undefined ? undefined : JSON.stringify(data),
    signal: AbortSignal.timeout(15000)
  });
  if (!response.ok) throw new Error(`API returned ${response.status}`);
  return method === 'DELETE' ? null : response.json();
}
function reset() {
  editing = null; input.value = ''; save.textContent = 'Add item'; cancel.hidden = true;
}
function render() {
  body.replaceChildren();
  items.forEach((item, index) => {
    const row = document.createElement('tr');
    const number = document.createElement('td'); number.textContent = index + 1;
    const title = document.createElement('td'); title.textContent = item.title;
    const actions = document.createElement('td');
    const edit = document.createElement('button'); edit.textContent = 'Edit';
    edit.setAttribute('aria-label', `Edit ${item.title}`);
    edit.onclick = () => { editing = item.key; input.value = item.title; save.textContent = 'Save changes'; cancel.hidden = false; input.focus(); };
    const remove = document.createElement('button'); remove.textContent = 'Delete';
    remove.setAttribute('aria-label', `Delete ${item.title}`);
    remove.onclick = () => run(async () => {
      await api(`/${item.id}`, 'DELETE');
      items = items.filter(value => value.key !== item.key);
      if (editing === item.key) reset();
      status.textContent = 'Deleted (demo API).';
    });
    edit.disabled = remove.disabled = busy;
    actions.append(edit, ' ', remove); row.append(number, title, actions); body.append(row);
  });
  if (!items.length) { const row = body.insertRow(); const cell = row.insertCell(); cell.colSpan = 3; cell.textContent = loaded ? 'No items. Add one above.' : 'No data loaded yet.'; }
  save.disabled = input.disabled = busy || !loaded; cancel.disabled = reload.disabled = busy;
}
async function run(action) {
  if (busy) return;
  busy = true; status.textContent = 'Working…'; render();
  try { await action(); } catch (error) { status.textContent = `Request failed: ${error.message}. Try again.`; }
  finally { busy = false; render(); }
}
async function load() {
  await run(async () => {
    const data = await api('?_limit=20');
    if (!Array.isArray(data) || data.length !== 20 || data.some(x => !Number.isInteger(x.id) || typeof x.title !== 'string')) throw new Error('Unexpected API data');
    items = data.map(item => ({...item, key: crypto.randomUUID()})); loaded = true; reset(); status.textContent = 'Loaded 20 API items.';
  });
}
form.onsubmit = event => {
  event.preventDefault();
  const title = input.value.trim();
  if (!title) { status.textContent = 'Enter a nonempty title.'; return; }
  run(async () => {
    const item = items.find(item => item.key === editing);
    if (item) {
      // PATCH works with the fake ID returned by POST; PUT would fail for that ID.
      await api(`/${item.id}`, 'PATCH', {title});
      items = items.map(value => value.key === item.key ? {...value, title} : value);
    } else {
      const result = await api('', 'POST', {title, body: '', userId: 1});
      if (!Number.isInteger(result.id)) throw new Error('Missing item ID');
      items = [{id: result.id, title, key: crypto.randomUUID()}, ...items];
    }
    reset(); status.textContent = 'Saved (demo API).';
  });
};
cancel.onclick = () => { reset(); input.focus(); };
reload.onclick = load;
load();

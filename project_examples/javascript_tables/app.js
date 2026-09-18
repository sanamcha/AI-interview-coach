const form = document.querySelector('#task-form');
const input = document.querySelector('#task');
const list = document.querySelector('#tasks');
const status = document.querySelector('#status');
let tasks = [];
let nextId = 1;

function render() {
  list.replaceChildren();
  status.textContent = tasks.length
    ? `${tasks.filter(task => !task.done).length} task(s) remaining`
    : 'No tasks yet. Add your first task.';
  for (const [index, task] of tasks.entries()) {
    const row = document.createElement('tr');
    const number = document.createElement('td');
    number.textContent = index + 1;
    const text = document.createElement('td');
    text.textContent = task.text;
    text.classList.toggle('done', task.done);
    const state = document.createElement('td');
    state.textContent = task.done ? 'Completed' : 'Active';
    const actions = document.createElement('td');
    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.textContent = task.done ? 'Undo' : 'Complete';
    toggle.setAttribute('aria-label', `${toggle.textContent} ${task.text}`);
    toggle.addEventListener('click', () => {
      task.done = !task.done;
      render();
      list.querySelectorAll('tr')[index].querySelector('button').focus();
    });
    const remove = document.createElement('button');
    remove.type = 'button';
    remove.textContent = 'Delete';
    remove.setAttribute('aria-label', `Delete ${task.text}`);
    remove.addEventListener('click', () => {
      tasks = tasks.filter(item => item.id !== task.id);
      render();
      input.focus();
    });
    actions.append(toggle, ' ', remove);
    row.append(number, text, state, actions);
    list.append(row);
  }
  if (!tasks.length) {
    const row = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 4;
    cell.textContent = 'No tasks yet.';
    row.append(cell);
    list.append(row);
  }
}

form.addEventListener('submit', event => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) {
    status.textContent = 'Enter a task before adding it.';
    input.focus();
    return;
  }
  tasks.push({id: nextId++, text, done: false});
  input.value = '';
  render();
  input.focus();
});
render();

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
  for (const task of tasks) {
    const row = document.createElement('li');
    const label = document.createElement('label');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = task.done;
    checkbox.addEventListener('change', () => {
      task.done = checkbox.checked;
      text.classList.toggle('done', task.done);
      status.textContent = `${tasks.filter(item => !item.done).length} task(s) remaining`;
    });
    const text = document.createElement('span');
    text.textContent = task.text;
    text.classList.toggle('done', task.done);
    label.append(checkbox, text);
    const remove = document.createElement('button');
    remove.type = 'button';
    remove.textContent = 'Delete';
    remove.setAttribute('aria-label', `Delete ${task.text}`);
    remove.addEventListener('click', () => {
      tasks = tasks.filter(item => item.id !== task.id);
      render();
      input.focus();
    });
    row.append(label, remove);
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

import { useRef, useState } from 'react';
import './App.css';

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [text, setText] = useState('');
  const [error, setError] = useState('');
  const nextId = useRef(1);
  const input = useRef(null);

  function addTask(event) {
    event.preventDefault();
    const value = text.trim();
    if (!value) {
      setError('Enter a task before adding it.');
      input.current.focus();
      return;
    }
    const task = { id: nextId.current++, text: value, done: false };
    setTasks(current => [...current, task]);
    setText('');
    setError('');
    input.current.focus();
  }

  function toggleTask(id) {
    setTasks(current => current.map(task =>
      task.id === id ? { ...task, done: !task.done } : task
    ));
  }

  function deleteTask(id) {
    setTasks(current => current.filter(task => task.id !== id));
    input.current.focus();
  }

  return (
    <main>
      <h1>To-Do List Tables</h1>
      <form onSubmit={addTask}>
        <label htmlFor="task">New task</label>
        <input id="task" ref={input} value={text} maxLength={120} required
          onChange={event => setText(event.target.value)} autoComplete="off" />
        <button>Add task</button>
      </form>
      <p role="status">{error || (tasks.length
        ? `${tasks.filter(task => !task.done).length} task(s) remaining`
        : 'No tasks yet. Add your first task.')}</p>
      <div className="table-scroll"><table>
        <caption>Your tasks</caption>
        <thead><tr><th scope="col">#</th><th scope="col">Task</th><th scope="col">Status</th><th scope="col">Actions</th></tr></thead>
        <tbody>
          {tasks.map((task, index) => (
            <tr key={task.id}>
              <td>{index + 1}</td>
              <td className={task.done ? 'done' : ''}>{task.text}</td>
              <td>{task.done ? 'Completed' : 'Active'}</td>
              <td>
                <button type="button" aria-label={`${task.done ? 'Undo' : 'Complete'} ${task.text}`}
                  onClick={() => toggleTask(task.id)}>{task.done ? 'Undo' : 'Complete'}</button>{' '}
                <button type="button" aria-label={`Delete ${task.text}`}
                  onClick={() => deleteTask(task.id)}>Delete</button>
              </td>
            </tr>
          ))}
          {!tasks.length && <tr><td colSpan={4}>No tasks yet.</td></tr>}
        </tbody>
      </table></div>
      <p>Tasks reset when you reload the page.</p>
    </main>
  );
}

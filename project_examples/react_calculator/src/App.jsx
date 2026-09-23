import {useState} from 'react';
import './App.css';
function calculate(left, operation, right) {
  if (!left.trim() || !right.trim()) throw new Error('Enter both numbers.');
  const a = Number(left), b = Number(right);
  if (!Number.isFinite(a) || !Number.isFinite(b)) throw new Error('Enter finite numbers.');
  let result;
  switch (operation) {
    case 'add': result = a + b; break;
    case 'subtract': result = a - b; break;
    case 'multiply': result = a * b; break;
    case 'divide':
      if (b === 0) throw new Error('Cannot divide by zero.');
      result = a / b; break;
    default: throw new Error('Choose a valid operation.');
  }
  if (!Number.isFinite(result)) throw new Error('Result is too large. Try smaller numbers.');
  return String(Number(result.toPrecision(12)));
}
export default function App() {
  const [left,setLeft] = useState(''), [right,setRight] = useState(''), [operation,setOperation] = useState('add');
  const [result,setResult] = useState('Enter two numbers to begin.');
  function submit(event) {
    event.preventDefault();
    try { setResult('Result: ' + calculate(left,operation,right)); }
    catch (error) { setResult(error.message); }
  }
  function clear() { setLeft(''); setRight(''); setOperation('add'); setResult('Enter two numbers to begin.'); }
  return <main><h1>Basic calculator</h1><form onSubmit={submit} onReset={clear}>
    <label htmlFor="left">First number</label><input id="left" type="number" step="any" required value={left} onChange={e=>setLeft(e.target.value)} />
    <label htmlFor="operation">Operation</label><select id="operation" value={operation} onChange={e=>setOperation(e.target.value)}><option value="add">+ Addition</option><option value="subtract">− Subtraction</option><option value="multiply">× Multiplication</option><option value="divide">÷ Division</option></select>
    <label htmlFor="right">Second number</label><input id="right" type="number" step="any" required value={right} onChange={e=>setRight(e.target.value)} />
    <button>Calculate</button><button type="reset">Clear</button>
    </form><p className="result" role="status">{result}</p><p>Supports decimals and negative numbers. Results are rounded to 12 significant digits.</p></main>;
}

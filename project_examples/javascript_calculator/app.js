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
const form = document.querySelector('#calculator'), output = document.querySelector('#result');
form.onsubmit = event => {
  event.preventDefault();
  try { output.textContent = 'Result: ' + calculate(form.elements.left.value, form.elements.operation.value, form.elements.right.value); }
  catch (error) { output.textContent = error.message; }
};
form.onreset = () => { output.textContent = 'Enter two numbers to begin.'; };

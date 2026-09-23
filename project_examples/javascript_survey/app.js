const yesQuestions = ["Do you enjoy reading books?", "Do you like trying new foods?", "Do you enjoy outdoor walks?", "Do you like listening to music?", "Would you like to learn a new language?"];
const textQuestions = ["What is your favorite hobby?", "Which place would you like to visit?", "What would you like to learn next?"];
function pickQuestions() {
  const pool = [...yesQuestions];
  const pick = () => pool.splice(Math.floor(Math.random() * pool.length), 1)[0];
  return [pick(), pick(), textQuestions[Math.floor(Math.random() * textQuestions.length)]];
}
let questions = pickQuestions(), answers = ['', '', ''];
const root = document.querySelector('#app');
function navigate(page) { location.hash = page; }
function render() {
  const results = location.hash === '#results' && answers.every(a => a.trim());
  const requested = Number(location.hash.replace('#question-', '')) || 1;
  const firstMissing = answers.findIndex(a => !a.trim());
  const step = Math.min(Math.max(requested - 1, 0), 2, firstMissing < 0 ? 2 : firstMissing);
  root.replaceChildren();
  const heading = document.createElement('h1');
  heading.textContent = results ? 'Your answers' : 'Simple survey';
  heading.tabIndex = -1; root.append(heading);
  if (results) {
    const list = document.createElement('dl');
    questions.forEach((question, i) => {
      const term = document.createElement('dt'); term.textContent = question;
      const answer = document.createElement('dd'); answer.textContent = answers[i];
      list.append(term, answer);
    });
    const back = document.createElement('button'); back.textContent = '← Back to Survey'; back.onclick = () => navigate('question-1');
    const restart = document.createElement('button'); restart.textContent = 'New random survey';
    restart.onclick = () => { questions = pickQuestions(); answers = ['', '', '']; navigate('question-1'); };
    root.append(list, back, restart);
  } else {
    const progress = document.createElement('p'); progress.textContent = `Question ${step + 1} of 3`;
    const form = document.createElement('form');
    const field = document.createElement('fieldset');
    const legend = document.createElement('legend'); legend.textContent = questions[step]; field.append(legend);
    if (step < 2) {
      for (const value of ['Yes', 'No']) {
        const label = document.createElement('label'); const input = document.createElement('input');
        input.type = 'radio'; input.name = 'answer'; input.value = value; input.required = true; input.checked = answers[step] === value;
        label.append(input, ' ' + value); field.append(label);
      }
    } else {
      const label = document.createElement('label'); label.textContent = 'Your answer'; label.htmlFor = 'answer';
      const input = document.createElement('input'); input.type = 'text'; input.id = 'answer'; input.name = 'answer'; input.maxLength = 200; input.required = true; input.value = answers[step];
      field.append(label, input);
    }
    const error = document.createElement('p'); error.className = 'error'; error.setAttribute('role', 'alert');
    const submit = document.createElement('button'); submit.textContent = step === 2 ? 'Submit survey' : 'Next →';
    form.append(field, error, submit);
    form.onsubmit = event => {
      event.preventDefault(); const value = new FormData(form).get('answer')?.trim();
      if (!value || (step < 2 && !['Yes', 'No'].includes(value))) { error.textContent = 'Please answer this question.'; return; }
      answers[step] = value;
      navigate(step === 2 ? 'results' : `question-${step + 2}`);
    };
    root.append(progress, form);
  }
  heading.focus();
}
window.addEventListener('hashchange', render);
render();

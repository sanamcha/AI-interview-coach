const bank = [{"question": "What is 6 \u00d7 7?", "choices": ["36", "42", "48"], "correct": 1}, {"question": "Which planet is closest to the Sun?", "choices": ["Venus", "Earth", "Mercury"], "correct": 2}, {"question": "How many sides does a triangle have?", "choices": ["3", "4", "5"], "correct": 0}, {"question": "Which animal is a mammal?", "choices": ["Shark", "Dolphin", "Trout"], "correct": 1}, {"question": "What is the capital of France?", "choices": ["Rome", "Madrid", "Paris"], "correct": 2}, {"question": "How many minutes are in an hour?", "choices": ["60", "100", "30"], "correct": 0}, {"question": "Which language runs natively in web browsers?", "choices": ["Python", "JavaScript", "Java"], "correct": 1}, {"question": "What does HTML describe?", "choices": ["Database queries", "Network encryption", "Web page structure"], "correct": 2}, {"question": "What is 15 + 8?", "choices": ["23", "21", "25"], "correct": 0}, {"question": "Which is a primary color of light?", "choices": ["Brown", "Red", "Orange"], "correct": 1}];
function pickQuestions() {
  const pool = [...bank];
  return Array.from({length: 5}, () => pool.splice(Math.floor(Math.random() * pool.length), 1)[0]);
}
let questions = pickQuestions(), answers = [];
const root = document.querySelector('#app');
function render() {
  root.replaceChildren();
  const heading = document.createElement('h1'); heading.tabIndex = -1;
  heading.textContent = answers.length === 5 ? 'Quiz results' : 'Quick quiz'; root.append(heading);
  if (answers.length === 5) {
    const score = answers.filter((answer, i) => answer === questions[i].correct).length;
    const result = document.createElement('p'); result.textContent = `Your score: ${score} / 5 · Percentage: ${score / 5 * 100}%`;
    const review = document.createElement('dl');
    questions.forEach((question, i) => {
      const term = document.createElement('dt'); term.textContent = question.question;
      const detail = document.createElement('dd'); detail.textContent = `Your answer: ${question.choices[answers[i]]} — ${answers[i] === question.correct ? 'Correct' : 'Incorrect'}. Correct answer: ${question.choices[question.correct]}`;
      review.append(term, detail);
    });
    const restart = document.createElement('button'); restart.textContent = 'Try a new quiz';
    restart.onclick = () => { questions = pickQuestions(); answers = []; render(); };
    root.append(result, review, restart);
  } else {
    const step = answers.length, question = questions[step];
    const progress = document.createElement('p'); progress.textContent = `Question ${step + 1} of 5`;
    const form = document.createElement('form'); const field = document.createElement('fieldset');
    const legend = document.createElement('legend'); legend.textContent = question.question; field.append(legend);
    question.choices.forEach((choice, index) => {
      const label = document.createElement('label'); const input = document.createElement('input');
      input.type = 'radio'; input.name = 'answer'; input.value = index; input.required = true;
      label.append(input, ' ' + choice); field.append(label);
    });
    const submit = document.createElement('button'); submit.textContent = step === 4 ? 'Finish quiz' : 'Next →';
    const error = document.createElement('p'); error.setAttribute('role', 'alert'); error.className = 'error';
    form.append(field, error, submit);
    form.onsubmit = event => {
      event.preventDefault();
      if (answers.length !== step) return;
      const raw = new FormData(form).get('answer'); const answer = Number(raw);
      if (raw === null || !Number.isInteger(answer) || answer < 0 || answer >= question.choices.length) { error.textContent = 'Choose an answer before continuing.'; return; }
      answers.push(answer); render();
    };
    root.append(progress, form);
  }
  heading.focus();
}
render();

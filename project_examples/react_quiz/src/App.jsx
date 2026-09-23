import {useEffect, useRef, useState} from 'react';
import './App.css';
const bank = [{"question": "What is 6 \u00d7 7?", "choices": ["36", "42", "48"], "correct": 1}, {"question": "Which planet is closest to the Sun?", "choices": ["Venus", "Earth", "Mercury"], "correct": 2}, {"question": "How many sides does a triangle have?", "choices": ["3", "4", "5"], "correct": 0}, {"question": "Which animal is a mammal?", "choices": ["Shark", "Dolphin", "Trout"], "correct": 1}, {"question": "What is the capital of France?", "choices": ["Rome", "Madrid", "Paris"], "correct": 2}, {"question": "How many minutes are in an hour?", "choices": ["60", "100", "30"], "correct": 0}, {"question": "Which language runs natively in web browsers?", "choices": ["Python", "JavaScript", "Java"], "correct": 1}, {"question": "What does HTML describe?", "choices": ["Database queries", "Network encryption", "Web page structure"], "correct": 2}, {"question": "What is 15 + 8?", "choices": ["23", "21", "25"], "correct": 0}, {"question": "Which is a primary color of light?", "choices": ["Brown", "Red", "Orange"], "correct": 1}];
function pickQuestions() {
  const pool = [...bank];
  return Array.from({length: 5}, () => pool.splice(Math.floor(Math.random() * pool.length), 1)[0]);
}
export default function App() {
  const [questions, setQuestions] = useState(pickQuestions);
  const [answers, setAnswers] = useState([]);
  const [selected, setSelected] = useState('');
  const [error, setError] = useState('');
  const heading = useRef(null);
  const step = answers.length;
  useEffect(() => { heading.current?.focus(); }, [step]);
  const score = answers.filter((answer, i) => answer === questions[i].correct).length;
  function submit(event) {
    event.preventDefault();
    if (selected === '') { setError('Choose an answer before continuing.'); return; }
    const answer = Number(selected);
    setAnswers(current => current.length === step ? [...current, answer] : current);
    setSelected(''); setError('');
  }
  function restart() { setQuestions(pickQuestions()); setAnswers([]); setSelected(''); setError(''); }
  return <main>
    <h1 ref={heading} tabIndex={-1}>{step === 5 ? 'Quiz results' : 'Quick quiz'}</h1>
    {step === 5 ? <>
      <p>Your score: <strong>{score} / 5</strong></p><p>Percentage: <strong>{score / 5 * 100}%</strong></p>
      <dl>{questions.map((question, i) => <div key={question.question}><dt>{question.question}</dt><dd>Your answer: {question.choices[answers[i]]} — {answers[i] === question.correct ? 'Correct' : 'Incorrect'}<br />Correct answer: {question.choices[question.correct]}</dd></div>)}</dl>
      <button onClick={restart}>Try a new quiz</button>
    </> : <>
      <p>Question {step + 1} of 5</p>
      <form onSubmit={submit}><fieldset><legend>{questions[step].question}</legend>
        {questions[step].choices.map((choice, index) => <label key={index}><input type="radio" name="answer" value={index} checked={selected === String(index)} required onChange={e => setSelected(e.target.value)} /> {choice}</label>)}
      </fieldset><p role="alert" className="error">{error}</p><button>{step === 4 ? 'Finish quiz' : 'Next →'}</button></form>
    </>}
  </main>;
}

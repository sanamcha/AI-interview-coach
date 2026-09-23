import {useEffect, useRef, useState} from 'react';
import './App.css';
const yesQuestions = ["Do you enjoy reading books?", "Do you like trying new foods?", "Do you enjoy outdoor walks?", "Do you like listening to music?", "Would you like to learn a new language?"];
const textQuestions = ["What is your favorite hobby?", "Which place would you like to visit?", "What would you like to learn next?"];
function pickQuestions() {
  const pool = [...yesQuestions];
  const pick = () => pool.splice(Math.floor(Math.random() * pool.length), 1)[0];
  return [pick(), pick(), textQuestions[Math.floor(Math.random() * textQuestions.length)]];
}
export default function App() {
  const [questions, setQuestions] = useState(pickQuestions);
  const [answers, setAnswers] = useState(['', '', '']);
  const [route, setRoute] = useState(location.hash);
  const [error, setError] = useState('');
  const heading = useRef(null);
  useEffect(() => {
    const update = () => { setRoute(location.hash); setError(''); };
    window.addEventListener('hashchange', update);
    return () => window.removeEventListener('hashchange', update);
  }, []);
  useEffect(() => { heading.current?.focus(); }, [route]);
  const complete = answers.every(answer => answer.trim());
  const results = route === '#results' && complete;
  const firstMissing = answers.findIndex(answer => !answer.trim());
  const step = Math.min(Math.max((Number(route.replace('#question-', '')) || 1) - 1, 0), 2, firstMissing < 0 ? 2 : firstMissing);
  function submit(event) {
    event.preventDefault();
    if (!answers[step].trim()) { setError('Please answer this question.'); return; }
    setAnswers(current => current.map((answer, i) => i === step ? answer.trim() : answer));
    location.hash = step === 2 ? 'results' : `question-${step + 2}`;
  }
  function change(value) { setAnswers(current => current.map((answer, i) => i === step ? value : answer)); }
  return <main>
    <h1 ref={heading} tabIndex={-1}>{results ? 'Your answers' : 'Simple survey'}</h1>
    {results ? <>
      <dl>{questions.map((question, i) => <div key={question}><dt>{question}</dt><dd>{answers[i]}</dd></div>)}</dl>
      <button onClick={() => { location.hash = 'question-1'; }}>← Back to Survey</button>
      <button onClick={() => { setQuestions(pickQuestions()); setAnswers(['', '', '']); location.hash = 'question-1'; }}>New random survey</button>
    </> : <>
      <p>Question {step + 1} of 3</p>
      <form onSubmit={submit}><fieldset><legend>{questions[step]}</legend>
        {step < 2 ? ['Yes', 'No'].map(value => <label key={value}>
          <input type="radio" name="answer" value={value} checked={answers[step] === value} required onChange={() => change(value)} /> {value}
        </label>) : <><label htmlFor="answer">Your answer</label><input id="answer" type="text" maxLength={200} required value={answers[step]} onChange={event => change(event.target.value)} /></>}
      </fieldset><p className="error" role="alert">{error}</p><button>{step === 2 ? 'Submit survey' : 'Next →'}</button></form>
    </>}
  </main>;
}

import {useState} from 'react';
import './App.css';
export default function App() {
  const [rating, setRating] = useState(0);
  return <main>
    <h1>5-Star Ratings</h1>
    <p id="help">Choose a star to rate. Click the selected rating again to clear it. Use Tab and Enter or Space with a keyboard.</p>
    <div className="stars" role="group" aria-label="Choose a rating" aria-describedby="help">
      {[1, 2, 3, 4, 5].map(value => <button key={value} type="button"
        className={`star${value <= rating ? ' selected' : ''}`}
        aria-label={`Rate ${value} out of 5`} aria-pressed={value === rating}
        onClick={() => setRating(current => current === value ? 0 : value)}>★</button>)}
    </div>
    <p role="status">{rating ? `${rating} out of 5 stars.` : 'No rating selected.'}</p>
    <p>Reloading clears this rating.</p>
  </main>;
}

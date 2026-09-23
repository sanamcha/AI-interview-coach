import {useEffect, useState} from 'react';
import './App.css';
const api = document.querySelector('meta[name=chat-api]')?.content || '/api/messages';
async function request(url, options) {
  const response = await fetch(url, {...options, signal: AbortSignal.timeout(10000)});
  if (!response.ok) throw new Error('Request failed. Please try again.');
  return response.json();
}
function Room({member, leave}) {
  const [messages, setMessages] = useState([]), [text, setText] = useState('');
  const [status, setStatus] = useState('Joined.'), [busy, setBusy] = useState(false);
  useEffect(() => {
    let stopped = false, timer;
    async function poll() {
      try {
        const data = await request(`${api}?room=${encodeURIComponent(member.room)}`);
        if (!stopped) setMessages(data);
      } catch (error) { if (!stopped) setStatus(error.message); }
      finally { if (!stopped) timer = setTimeout(poll, 1500); }
    }
    poll();
    return () => { stopped = true; clearTimeout(timer); };
  }, [member.room]);
  async function send(event) {
    event.preventDefault(); if (!text.trim() || busy) return;
    setBusy(true);
    try {
      await request(api, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({...member, text:text.trim()})});
      setText(''); setStatus('Sent.');
    } catch (error) { setStatus(error.message); }
    finally { setBusy(false); }
  }
  return <section><h2>{member.room} · {member.name}</h2><button onClick={leave}>Leave room</button>
    <div className="messages" role="log" aria-label="Messages" aria-live="polite">{messages.map(message => <p key={message.id}><strong>{message.name}: </strong>{message.text}</p>)}</div>
    <form onSubmit={send}><label>Message <input value={text} onChange={e => setText(e.target.value)} maxLength={500} required autoComplete="off" /></label><button disabled={busy}>Send</button></form><p role="status">{status}</p></section>;
}
export default function App() {
  const [member, setMember] = useState(null), [error, setError] = useState('');
  function join(event) {
    event.preventDefault(); const data = new FormData(event.currentTarget);
    const name = data.get('name').trim(), room = data.get('room').trim();
    if (!name || !room) { setError('Enter a name and room.'); return; }
    setError(''); setMember({name, room});
  }
  return <main><h1>Shared-room chat</h1><p>Open two tabs and join the same room with different names. Demo names are not verified; anyone with the room name can join.</p>
    {member ? <Room member={member} leave={() => setMember(null)} /> : <form onSubmit={join}><label>Your name <input name="name" maxLength={30} required /></label><label>Room <input name="room" maxLength={40} defaultValue="practice" required /></label><button>Join room</button><p role="alert">{error}</p></form>}
  </main>;
}

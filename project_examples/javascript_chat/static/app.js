const api = document.querySelector('meta[name=chat-api]').content;
const join = document.querySelector('#join'), chat = document.querySelector('#chat');
const send = document.querySelector('#send'), log = document.querySelector('#messages');
const status = document.querySelector('#status');
let member = null, timer = null, generation = 0, lastId = 0;
async function request(url, options) {
  const response = await fetch(url, {...options, signal: AbortSignal.timeout(10000)});
  if (!response.ok) throw new Error('Request failed. Check your connection and try again.');
  return response.json();
}
async function poll(version) {
  try {
    const messages = await request(`${api}?room=${encodeURIComponent(member.room)}`);
    if (version !== generation) return;
    for (const message of messages.filter(item => item.id > lastId)) {
      const row = document.createElement('p');
      const name = document.createElement('strong'); name.textContent = message.name + ': ';
      row.append(name, document.createTextNode(message.text)); log.append(row);
      lastId = message.id;
    }
    while (log.children.length > 100) log.firstElementChild.remove();
  } catch (error) { if (version === generation) status.textContent = error.message; }
  finally { if (version === generation) timer = setTimeout(() => poll(version), 1500); }
}
join.onsubmit = event => {
  event.preventDefault();
  const data = new FormData(join), name = data.get('name').trim(), room = data.get('room').trim();
  if (!name || !room) { status.textContent = 'Enter a name and room.'; return; }
  member = {name, room}; generation++; lastId = 0; log.replaceChildren();
  join.hidden = true; chat.hidden = false; status.textContent = 'Joined. Messages refresh automatically.';
  document.querySelector('#room-title').textContent = `${room} · ${name}`;
  send.elements.text.focus(); poll(generation);
};
document.querySelector('#leave').onclick = () => {
  generation++; clearTimeout(timer); member = null; chat.hidden = true; join.hidden = false; status.textContent = ''; join.elements.name.focus();
};
send.onsubmit = async event => {
  event.preventDefault();
  const text = send.elements.text.value.trim();
  if (!text || !member) return;
  const version = generation, button = send.querySelector('button'); button.disabled = true;
  try {
    await request(api, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({...member, text})});
    if (version === generation) { send.elements.text.value = ''; status.textContent = 'Sent.'; }
  } catch (error) { if (version === generation) status.textContent = error.message; }
  finally { button.disabled = false; }
};

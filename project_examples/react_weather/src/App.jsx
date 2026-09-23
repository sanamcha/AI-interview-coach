import {useRef, useState} from 'react';
import './App.css';
const descriptions = {0:'Clear sky',1:'Mainly clear',2:'Partly cloudy',3:'Overcast',45:'Fog',48:'Rime fog',51:'Light drizzle',53:'Drizzle',55:'Heavy drizzle',56:'Freezing drizzle',57:'Heavy freezing drizzle',61:'Light rain',63:'Rain',65:'Heavy rain',66:'Freezing rain',67:'Heavy freezing rain',71:'Light snow',73:'Snow',75:'Heavy snow',77:'Snow grains',80:'Light showers',81:'Showers',82:'Heavy showers',85:'Snow showers',86:'Heavy snow showers',95:'Thunderstorm',96:'Thunderstorm with hail',99:'Thunderstorm with heavy hail'};
async function getJSON(url) {
  const response = await fetch(url, {signal: AbortSignal.timeout(15000)});
  if (!response.ok) throw new Error('Weather service unavailable. Please try again.');
  return response.json();
}
async function weatherFor(city) {
  const geo = await getJSON('https://geocoding-api.open-meteo.com/v1/search?' + new URLSearchParams({name:city,count:1,language:'en'}));
  const place = geo.results?.[0];
  if (!place) throw new Error('City not found. Check the spelling and try again.');
  const data = await getJSON('https://api.open-meteo.com/v1/forecast?' + new URLSearchParams({latitude:place.latitude,longitude:place.longitude,current:'temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m',timezone:'auto'}));
  const current = data.current;
  if (!current || !Number.isFinite(current.temperature_2m)) throw new Error('Current weather is unavailable for this city.');
  return {place:[place.name,place.admin1,place.country].filter(Boolean).join(', '), current, timezone:data.timezone, description:descriptions[current.weather_code] || 'Unknown conditions'};
}
function display(value, unit) { return value == null ? 'Unavailable' : `${value} ${unit}`; }
export default function App() {
  const [city,setCity] = useState(''), [result,setResult] = useState(null), [status,setStatus] = useState(''), [busy,setBusy] = useState(false);
  const lock = useRef(false);
  async function search(event) {
    event.preventDefault(); if (lock.current) return;
    if (!city.trim()) { setStatus('Enter a city name.'); return; }
    lock.current = true; setBusy(true); setResult(null); setStatus('Loading weather…');
    try { setResult(await weatherFor(city.trim())); setStatus('Weather loaded.'); }
    catch (error) { setStatus(error.message); }
    finally { lock.current = false; setBusy(false); }
  }
  return <main><h1>Current weather</h1><form onSubmit={search}><label htmlFor="city">City name</label><input id="city" type="text" value={city} onChange={e=>setCity(e.target.value)} maxLength={100} required placeholder="e.g. London" /><button disabled={busy}>Search weather</button></form><p role="status">{status}</p>
    {result && <section className="weather"><h2>{result.place}</h2><p>{result.description}</p><p>Temperature: {display(result.current.temperature_2m,'°C')}</p><p>Feels like: {display(result.current.apparent_temperature,'°C')}</p><p>Humidity: {display(result.current.relative_humidity_2m,'%')}</p><p>Wind: {display(result.current.wind_speed_10m,'km/h')}</p><p>Updated: {result.current.time} ({result.timezone})</p></section>}
    <p>Showing the first matching city. Check its region and country.</p><p>Weather data: <a href="https://open-meteo.com/">Open-Meteo</a> · Locations: GeoNames. Current conditions are model estimates.</p></main>;
}

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
const form = document.querySelector('#search'), status = document.querySelector('#status'), panel = document.querySelector('#weather');
let busy = false;
form.onsubmit = async event => {
  event.preventDefault(); if (busy) return;
  const city = form.elements.city.value.trim();
  if (!city) { status.textContent = 'Enter a city name.'; return; }
  busy = true; form.querySelector('button').disabled = true; panel.hidden = true; panel.replaceChildren(); status.textContent = 'Loading weather…';
  try {
    const result = await weatherFor(city), current = result.current;
    const heading = document.createElement('h2'); heading.textContent = result.place; panel.append(heading);
    for (const line of [result.description,`Temperature: ${display(current.temperature_2m,'°C')}`,`Feels like: ${display(current.apparent_temperature,'°C')}`,`Humidity: ${display(current.relative_humidity_2m,'%')}`,`Wind: ${display(current.wind_speed_10m,'km/h')}`,`Updated: ${current.time} (${result.timezone})`]) {
      const p = document.createElement('p'); p.textContent = line; panel.append(p);
    }
    panel.hidden = false; status.textContent = 'Weather loaded.';
  } catch (error) { status.textContent = error.message; }
  finally { busy = false; form.querySelector('button').disabled = false; }
};

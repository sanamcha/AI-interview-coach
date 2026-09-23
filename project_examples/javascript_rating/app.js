let rating = 0;
const stars = document.querySelectorAll('.star');
const status = document.querySelector('#status');
for (const star of stars) {
  star.addEventListener('click', () => {
    const value = Number(star.dataset.value);
    rating = rating === value ? 0 : value;
    for (const button of stars) {
      const number = Number(button.dataset.value);
      button.classList.toggle('selected', number <= rating);
      button.setAttribute('aria-pressed', String(number === rating));
    }
    status.textContent = rating ? `${rating} out of 5 stars.` : 'No rating selected.';
  });
}

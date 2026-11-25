// Events page: events whose end time has passed move to "Past events", newest first.
(() => {
  const upcoming = document.getElementById('evUpcoming');
  if (!upcoming) return;
  const now = Date.now();
  const past = [...upcoming.querySelectorAll('.ev-card')].filter(card => new Date(card.dataset.end).getTime() < now);
  if (past.length) {
    const grid = document.getElementById('evPast');
    past.reverse().forEach(card => {
      card.classList.add('is-past');
      const cta = card.querySelector('.ev-cta');
      if (cta) cta.innerHTML = '<span class="button ev-off" aria-disabled="true">This event has finished</span>';
      grid.appendChild(card);
    });
    document.getElementById('evPastWrap').hidden = false;
  }
  document.getElementById('evEmpty').hidden = upcoming.querySelector('.ev-card') !== null;
})();

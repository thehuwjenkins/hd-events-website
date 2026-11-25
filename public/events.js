// Events page. Events come from two places:
//  - EVENTS in tools/site_content.py (built into the page), and
//  - events published from HD Events HQ (Event Planner > Website), loaded live from HQ.
// Events whose end time has passed move to "Past events", newest first.
(() => {
  const upcoming = document.getElementById('evUpcoming');
  if (!upcoming) return;
  const FEED = 'https://hq.hd-events.co.uk/q/events.json';
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const parse = s => new Date(s.length === 10 ? s + 'T00:00' : s);
  const endOf = e => e.end ? parse(e.end) : new Date(parse(e.start).setHours(23, 59, 0, 0));
  const day = d => d.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'long', year: 'numeric' }).replace(',', '');
  const time = d => { const h = d.getHours() % 12 || 12, m = d.getMinutes(); return h + (m ? ':' + String(m).padStart(2, '0') : '') + (d.getHours() < 12 ? 'am' : 'pm'); };
  function nice(e) {
    const s = parse(e.start), end = endOf(e);
    if (end.toDateString() !== s.toDateString()) return s.toLocaleDateString('en-GB', { weekday: 'short' }) + ' ' + s.getDate() + ' – ' + day(end);
    return day(s) + (e.start.length > 10 && (s.getHours() || s.getMinutes()) ? ' · ' + time(s) : '');
  }
  function card(e) {
    const where = [e.venue, e.town].filter(Boolean).join(', ');
    const status = (e.status || '').toLowerCase();
    const poster = e.poster ? `<img src="${esc(e.poster)}" alt="Poster for ${esc(e.title)}" loading="lazy">` : `<div class="ev-noposter" aria-hidden="true"><span>${esc(e.title)}</span></div>`;
    const cta = status === 'cancelled' ? '<span class="button ev-off" aria-disabled="true">Cancelled</span>'
      : status === 'sold out' ? '<span class="button ev-off" aria-disabled="true">Sold out</span>'
      : e.tickets ? `<a class="button solid ev-tickets" href="${esc(e.tickets)}" target="_blank" rel="noopener">Buy tickets <span>↗</span></a>`
      : '<span class="button ev-off" aria-disabled="true">Tickets coming soon</span>';
    const el = document.createElement('article');
    el.className = 'ev-card';
    el.dataset.end = endOf(e).toISOString();
    el.dataset.start = parse(e.start).toISOString();
    el.innerHTML = `<figure class="ev-poster">${poster}${status ? `<span class="ev-status">${esc(status.replace(/\b\w/g, c => c.toUpperCase()))}</span>` : ''}</figure>
      <div class="ev-body"><p class="ev-date"><time datetime="${esc(e.start)}">${esc(nice(e))}</time></p><h3>${esc(e.title)}</h3>
      ${where ? `<p class="ev-where">${esc(where)}</p>` : ''}<p class="ev-desc">${esc(e.description)}</p><div class="ev-cta">${cta}${e.price ? `<span class="ev-price">${esc(e.price)}</span>` : ''}</div></div>`;
    return el;
  }
  function schema(list) {
    if (!list.length) return;
    const s = document.createElement('script');
    s.type = 'application/ld+json';
    s.textContent = JSON.stringify({ '@context': 'https://schema.org', '@graph': list.map(e => {
      const st = (e.status || '').toLowerCase(), m = /£\s*([\d.,]+)/.exec(e.price || '');
      return { '@type': 'Event', name: e.title, startDate: e.start, endDate: endOf(e).toISOString(),
        eventStatus: st === 'cancelled' ? 'https://schema.org/EventCancelled' : 'https://schema.org/EventScheduled',
        eventAttendanceMode: 'https://schema.org/OfflineEventAttendanceMode',
        location: { '@type': 'Place', name: e.venue || e.town || '', address: e.address || [e.venue, e.town].filter(Boolean).join(', ') },
        description: e.description, ...(e.poster ? { image: [e.poster] } : {}),
        organizer: { '@type': 'Organization', name: 'HD Events', url: 'https://www.hd-events.co.uk/' },
        ...(e.tickets ? { offers: { '@type': 'Offer', url: e.tickets, priceCurrency: 'GBP', availability: st === 'sold out' ? 'https://schema.org/SoldOut' : 'https://schema.org/InStock', ...(m ? { price: m[1].replace(/,/g, '') } : /free/i.test(e.price || '') ? { price: '0' } : {}) } } : {}) };
    }) }).replace(/</g, '\\u003c');
    document.head.appendChild(s);
  }
  function arrange() {
    const now = Date.now();
    const cards = [...document.querySelectorAll('#evUpcoming .ev-card, #evPast .ev-card')];
    const past = cards.filter(c => new Date(c.dataset.end).getTime() < now).sort((a, b) => new Date(b.dataset.end) - new Date(a.dataset.end));
    const next = cards.filter(c => !past.includes(c)).sort((a, b) => new Date(a.dataset.start || a.dataset.end) - new Date(b.dataset.start || b.dataset.end));
    next.forEach(c => upcoming.appendChild(c));
    const grid = document.getElementById('evPast');
    past.forEach(c => {
      c.classList.add('is-past');
      const cta = c.querySelector('.ev-cta');
      if (cta) cta.innerHTML = '<span class="button ev-off" aria-disabled="true">This event has finished</span>';
      grid.appendChild(c);
    });
    document.getElementById('evPastWrap').hidden = !past.length;
    document.getElementById('evEmpty').hidden = next.length > 0;
  }
  arrange();
  fetch(FEED, { mode: 'cors', credentials: 'omit' })
    .then(r => (r.ok ? r.json() : { events: [] }))
    .then(({ events = [] }) => {
      const list = events.filter(e => e && e.title && e.start);
      list.forEach(e => upcoming.appendChild(card(e)));
      schema(list);
      arrange();
    })
    .catch(() => {});
})();

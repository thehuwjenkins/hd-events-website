// Book a driver: checks the required details, then writes them up as a WhatsApp message or email.
(() => {
  const form = document.getElementById('dqForm');
  if (!form) return;
  const wa = document.getElementById('dqWhatsApp'), mail = document.getElementById('dqEmail'), hint = document.getElementById('dqHint');
  const message = () => {
    const f = Object.fromEntries(new FormData(form));
    const date = f.date ? new Date(f.date + 'T12:00').toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'long', year: 'numeric' }) : '';
    const needs = [f.setup && 'set up and test on arrival', f.crew && 'stay on as crew', f.other && 'collect from / return to another hire company', f.handball && 'extra hands to load in or out'].filter(Boolean);
    const stops = { 0: 'none', 1: '1', 2: '2', 3: '3 or more' }[f.stops] || 'none';
    return { date, text: [
      'Hi HD Events, I would like to book a driver.', '',
      'Company: ' + f.company, 'Contact: ' + f.name, 'Phone: ' + f.phone, 'Email: ' + f.email, '',
      'Collection: ' + f.from, 'Drop-off: ' + f.to, 'Date: ' + date, 'Delivery time: ' + (f.time || 'flexible'),
      'Collect back: ' + f.collect, 'Extra stops: ' + stops, '',
      'Equipment: ' + f.load,
      'We need: ' + (needs.length ? needs.join(', ') : 'delivery and collection only'),
      'Other requirements: ' + (f.needs || 'none'),
    ].join('\n') };
  };
  const send = (e, how) => {
    const missing = [...form.querySelectorAll('[required]')].filter(el => !el.checkValidity());
    if (missing.length) {
      e.preventDefault();
      hint.textContent = 'Please fill in the ' + missing.length + ' required field' + (missing.length > 1 ? 's' : '') + ' marked in red.';
      hint.classList.add('warn');
      form.classList.add('checked');
      missing[0].focus();
      return;
    }
    const { date, text } = message();
    if (how === 'wa') wa.href = 'https://wa.me/447930547024?text=' + encodeURIComponent(text);
    else mail.href = 'mailto:hello@hd-events.co.uk?subject=' + encodeURIComponent('Book a driver: ' + (form.company.value || '') + (date ? ', ' + date : '')) + '&body=' + encodeURIComponent(text);
  };
  wa.addEventListener('click', e => send(e, 'wa'));
  mail.addEventListener('click', e => send(e, 'mail'));
  form.addEventListener('input', () => { if (form.classList.contains('checked') && form.checkValidity()) { hint.textContent = 'All set. Choose WhatsApp or email to send.'; hint.classList.remove('warn'); } });
  form.addEventListener('submit', e => e.preventDefault());
})();

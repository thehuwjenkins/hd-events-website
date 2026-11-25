// AV delivery page: turns the delivery form into a ready-written WhatsApp message or email.
(() => {
  const form = document.getElementById('dqForm');
  if (!form) return;
  const wa = document.getElementById('dqWhatsApp'), mail = document.getElementById('dqEmail');
  const update = () => {
    const f = Object.fromEntries(new FormData(form));
    const date = f.date ? new Date(f.date + 'T12:00').toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'long', year: 'numeric' }) : '';
    const tech = [f.setup && 'set up and test on arrival', f.crew && 'stay on as crew', f.other && 'collect from / return to another hire company'].filter(Boolean);
    const stops = { 0: 'none', 1: '1', 2: '2', 3: '3 or more' }[f.stops] || 'none';
    const text = [
      'Hi HD Events, please can I have a price for a delivery.', '',
      'Collect from: ' + (f.from || ''),
      'Deliver to: ' + (f.to || ''),
      'Date: ' + date,
      'Delivery time: ' + (f.time || ''),
      'Collection: ' + f.collect,
      'Extra stops: ' + stops,
      'What is being moved: ' + (f.load || ''),
      'Technician to: ' + (tech.length ? tech.join(', ') : 'deliver and collect only'),
    ].join('\n');
    wa.href = 'https://wa.me/447930547024?text=' + encodeURIComponent(text);
    mail.href = 'mailto:hello@hd-events.co.uk?subject=' + encodeURIComponent('Delivery price' + (date ? ' for ' + date : '')) + '&body=' + encodeURIComponent(text);
  };
  form.addEventListener('input', update);
  form.addEventListener('change', update);
  form.addEventListener('submit', e => e.preventDefault());
  update();
})();

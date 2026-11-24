// Digital lectern configurator: running total and a ready-written spec for WhatsApp or email.
(() => {
  const form = document.querySelector('.lx-config');
  if (!form) return;
  const data = JSON.parse(document.getElementById('lxData').textContent);
  const fmt = n => '£' + n.toLocaleString('en-GB');
  const update = () => {
    const picked = [...form.querySelectorAll('input:checked')];
    let total = data.base, poa = [];
    picked.forEach(i => { if (i.dataset.price) total += Number(i.dataset.price); else poa.push(i.dataset.name); });
    document.getElementById('lxTotal').textContent = fmt(total);
    document.getElementById('lxNote').textContent = 'ex VAT' + (poa.length ? ' + ' + poa.length + ' item' + (poa.length > 1 ? 's' : '') + ' priced on request' : '');
    const lines = ['Hi HD Events, I would like a quote for a digital lectern.', '', 'Build: ' + data.name + ' (from ' + fmt(data.base) + ')'];
    if (picked.length) { lines.push('Upgrades:'); picked.forEach(i => lines.push('- ' + i.dataset.name)); }
    lines.push('', 'Estimated from ' + fmt(total) + ' ex VAT', '', 'Buy or hire:', 'Venue / location:', 'Date needed:');
    const text = lines.join('\n');
    document.getElementById('lxWhatsApp').href = 'https://wa.me/447930547024?text=' + encodeURIComponent(text);
    document.getElementById('lxEmail').href = 'mailto:hello@hd-events.co.uk?subject=' + encodeURIComponent('Digital lectern quote') + '&body=' + encodeURIComponent(text);
  };
  form.addEventListener('change', event => {
    const choice = event.target;
    if (choice.matches('input[data-monitor]:checked')) {
      form.querySelectorAll('input[data-monitor]').forEach(input => {
        if (input !== choice) input.checked = false;
      });
    }
    update();
  });
  update();
})();

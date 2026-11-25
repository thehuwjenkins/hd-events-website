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
    const mini = document.getElementById('lxMiniTotal');
    if (mini) {
      mini.textContent = fmt(total);
      document.getElementById('lxMiniCount').textContent = picked.length ? 'Your build · ' + picked.length + ' upgrade' + (picked.length > 1 ? 's' : '') : 'Standard build';
    }
    document.getElementById('lxNote').textContent = 'ex VAT' + (poa.length ? ' + ' + poa.length + ' item' + (poa.length > 1 ? 's' : '') + ' priced on request' : '');
    const lines = ['Hi HD Events, I would like a quote for a digital lectern.', '', 'Build: ' + data.name + ' (from ' + fmt(data.base) + ')'];
    if (picked.length) { lines.push('Upgrades:'); picked.forEach(i => lines.push('- ' + i.dataset.name)); }
    lines.push('', 'Estimated from ' + fmt(total) + ' ex VAT', '', 'Buy or hire:', 'Venue / location:', 'Date needed:');
    const spec = document.getElementById('lxSpec');
    if (spec) spec.value = [data.name + ' — ' + fmt(data.base), ...picked.map(i => i.dataset.name + ' — ' + (i.dataset.price ? fmt(Number(i.dataset.price)) : 'price on request')), 'Estimated purchase price from ' + fmt(total) + ' ex VAT, excluding delivery'].join('\n');
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
  const dialog = document.getElementById('enquiry');
  const summary = document.getElementById('lxBuildSummary');
  const spec = document.getElementById('lxSpec');
  const status = document.getElementById('lxCopyStatus');
  async function copySpec() {
    try {
      await navigator.clipboard.writeText(spec.value);
      status.textContent = 'Build copied. Paste it into your enquiry details below.';
    } catch {
      spec.focus();
      spec.select();
      status.textContent = 'Copy the selected build and paste it into your enquiry details below.';
    }
  }
  document.getElementById('lxEnquire')?.addEventListener('click', () => {
    summary.hidden = false;
    dialog.showModal();
    copySpec();
  });
  document.getElementById('lxCopy')?.addEventListener('click', copySpec);
  dialog?.addEventListener('close', () => { if (summary) summary.hidden = true; });
  // On phones the total sits below a long list, so a small bar keeps it in view while choosing.
  const bar = document.getElementById('lxMini'), send = document.getElementById('lxSend');
  if (bar && 'IntersectionObserver' in window) {
    let inForm = false, atTotal = false;
    const show = () => { bar.hidden = !(inForm && !atTotal); };
    new IntersectionObserver(([en]) => { inForm = en.isIntersecting; show(); }).observe(form);
    new IntersectionObserver(([en]) => { atTotal = en.isIntersecting; show(); }).observe(send);
  }
  update();
})();

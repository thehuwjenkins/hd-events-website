// Top menu: mobile open/close, "More" dropdown, and a solid header once the page scrolls.
(() => {
  const header = document.querySelector('.site-header');
  if (!header) return;
  const toggle = header.querySelector('.menu-toggle');
  const setOpen = open => {
    document.body.classList.toggle('menu-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.querySelector('.label').textContent = open ? 'Close' : 'Menu';
  };
  toggle.addEventListener('click', () => setOpen(!document.body.classList.contains('menu-open')));
  header.querySelectorAll('.has-sub > button').forEach(btn => btn.addEventListener('click', () => {
    btn.setAttribute('aria-expanded', String(btn.getAttribute('aria-expanded') !== 'true'));
  }));
  // Close the menu after choosing a link (including same-page links like /#work)
  header.querySelectorAll('.main-nav a').forEach(a => a.addEventListener('click', () => setOpen(false)));
  document.addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    setOpen(false);
    header.querySelectorAll('.has-sub > button').forEach(b => b.setAttribute('aria-expanded', 'false'));
  });
  document.addEventListener('click', e => {
    if (!e.target.closest('.has-sub')) header.querySelectorAll('.has-sub > button').forEach(b => b.setAttribute('aria-expanded', 'false'));
  });
  const onScroll = () => header.classList.toggle('scrolled', scrollY > 40);
  onScroll(); addEventListener('scroll', onScroll, { passive: true });
})();

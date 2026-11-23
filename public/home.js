// Home page: gentle fade-up of sections as they scroll into view.
document.documentElement.classList.add('js');
const revealables = document.querySelectorAll('.section-intro, .package, .kit-card, .gallery figure, .reviews blockquote, .steps li, .service-cards a, .promises li');
revealables.forEach(el => el.classList.add('reveal-up'));
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px' });
  revealables.forEach(el => io.observe(el));
} else revealables.forEach(el => el.classList.add('in'));

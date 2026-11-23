const slides = Array.from(document.querySelectorAll('[data-slide]'));
const previous = document.querySelector('#previous');
const next = document.querySelector('#next');
const jump = document.querySelector('#jump');
const counter = document.querySelector('#counter');
let current = 0;

function renderSlide(focusHeading) {
  const target = slides.findIndex(slide => '#' + slide.id === location.hash);
  if (target === -1 && location.hash) history.replaceState(null, '', '#intro');
  current = Math.max(target, 0);
  slides.forEach((slide, index) => { slide.hidden = index !== current; });
  jump.value = slides[current].id;
  counter.textContent = (current + 1) + ' / ' + slides.length;
  previous.disabled = current === 0;
  next.disabled = current === slides.length - 1;
  if (focusHeading) {
    slides[current].querySelector('h1').focus({ preventScroll: true });
    window.scrollTo(0, 0);
  }
}

function navigate(index) {
  if (index >= 0 && index < slides.length && index !== current) {
    location.hash = slides[index].id;
  }
}

previous.addEventListener('click', () => navigate(current - 1));
next.addEventListener('click', () => navigate(current + 1));
jump.addEventListener('change', () => { location.hash = jump.value; });
window.addEventListener('hashchange', () => renderSlide(true));
document.addEventListener('keydown', event => {
  if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey ||
      event.target.closest('select, input, textarea, [contenteditable]')) return;
  const destinations = { ArrowLeft: current - 1, ArrowRight: current + 1, Home: 0, End: slides.length - 1 };
  if (Object.hasOwn(destinations, event.key)) {
    event.preventDefault();
    navigate(destinations[event.key]);
  }
});
renderSlide(false);
document.querySelector('.controls').hidden = false;


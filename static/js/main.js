const burger = document.querySelector('.burger');
const navLinks = document.querySelector('.nav-links');

burger.addEventListener('click', (e) => {
  e.stopPropagation(); // Ngăn chặn sự kiện lan ra ngoài
  navLinks.classList.toggle('active');
  const expanded = burger.getAttribute('aria-expanded') === 'true';
  burger.setAttribute('aria-expanded', !expanded);
});

document.addEventListener('click', (e) => {
  // Kiểm tra nếu click không nằm trong .nav-links hoặc .burger
  if (!navLinks.contains(e.target) && !burger.contains(e.target)) {
    if (navLinks.classList.contains('active')) {
      navLinks.classList.remove('active');
      burger.setAttribute('aria-expanded', 'false');
    }
  }
});

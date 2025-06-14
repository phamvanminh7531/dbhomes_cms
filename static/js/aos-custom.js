document.addEventListener('DOMContentLoaded', function () {
  if (window.innerWidth <= 768) {
    document.querySelectorAll('[data-aos="fade-left"], [data-aos="fade-right"]').forEach(el => {
      el.setAttribute('data-aos', 'fade-up');
    });
  }
});

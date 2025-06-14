document.addEventListener('DOMContentLoaded', () => {
  const slider = document.querySelector('.partner-logos');
  let isDown = false;
  let startX;
  let scrollLeft;
  let ticking = false;

  slider.addEventListener('mousedown', (e) => {
    isDown = true;
    startX = e.pageX - slider.offsetLeft;
    scrollLeft = slider.scrollLeft;
    slider.style.cursor = 'grabbing';
  });

  slider.addEventListener('mouseup', () => {
    isDown = false;
    slider.style.cursor = 'grab';
  });

  slider.addEventListener('mouseleave', () => {
    isDown = false;
    slider.style.cursor = 'grab';
  });

  slider.addEventListener('mousemove', (e) => {
    if (!isDown) return;

    if (!ticking) {
      window.requestAnimationFrame(() => {
        const x = e.pageX - slider.offsetLeft;
        const walk = (x - startX) * 1;  // điều chỉnh hệ số cho phù hợp
        slider.scrollLeft = scrollLeft - walk;
        ticking = false;
      });
      ticking = true;
    }
  });
});





window.addEventListener('load', resizePartnerLogos);
window.addEventListener('resize', resizePartnerLogos);

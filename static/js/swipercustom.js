function initSwiper(swiperSelector, paginationOptions = {}) {
  const swiperEl = document.querySelector(swiperSelector);
  if (!swiperEl) {
    console.warn(`Swiper element "${swiperSelector}" not found.`);
    return;  // Thoát sớm nếu không có element
  }

  const dots = paginationOptions.dotsSelector ? document.querySelectorAll(paginationOptions.dotsSelector) : null;
  const prevArrow = paginationOptions.prevArrowSelector ? document.querySelector(paginationOptions.prevArrowSelector) : null;
  const nextArrow = paginationOptions.nextArrowSelector ? document.querySelector(paginationOptions.nextArrowSelector) : null;

  const updateDots = () => {
    if (!swiperEl.swiper || !dots) return;
    const activeIndex = swiperEl.swiper.realIndex ?? swiperEl.swiper.activeIndex;
    dots.forEach(dot => dot.classList.remove('active'));
    if (dots[activeIndex]) dots[activeIndex].classList.add('active');
  };

  const waitForSwiper = setInterval(() => {
    if (swiperEl.swiper) {
      clearInterval(waitForSwiper);
      const swiperInstance = swiperEl.swiper;

      if (dots && dots.length > 0) {
        dots.forEach((dot, index) => {
          dot.addEventListener('click', () => {
            swiperInstance.slideTo(index);
          });
        });
      }

      if (prevArrow) {
        prevArrow.addEventListener('click', () => {
          if (!swiperInstance.isBeginning) {
            swiperInstance.slidePrev();
          }
        });
      }

      if (nextArrow) {
        nextArrow.addEventListener('click', () => {
          if (!swiperInstance.isEnd) {
            swiperInstance.slideNext();
          }
        });
      }

      swiperInstance.on('slideChange', updateDots);
      updateDots();
    }
  }, 100);
}

// Khởi tạo các swiper
initSwiper('.mySwiper', {
  dotsSelector: '.highlighted-projects .dot',
  prevArrowSelector: '.highlighted-projects .arrow.prev',
  nextArrowSelector: '.highlighted-projects .arrow.next'
});

initSwiper('.mySwiper2', {
  dotsSelector: '.feedback-news-section .dot',
  prevArrowSelector: '.feedback-news-section .arrow.prev',
  nextArrowSelector: '.feedback-news-section .arrow.next'
});

function initSwiper(swiperSelector, paginationOptions = {}) {
  const swiperEl = document.querySelector(swiperSelector);
  if (!swiperEl) {
    console.warn(`Swiper element "${swiperSelector}" not found.`);
    return;
  }

  const paginationContainer = paginationOptions.paginationContainerSelector
    ? document.querySelector(paginationOptions.paginationContainerSelector)
    : null;

  const prevArrow = paginationOptions.prevArrowSelector
    ? document.querySelector(paginationOptions.prevArrowSelector)
    : null;

  const nextArrow = paginationOptions.nextArrowSelector
    ? document.querySelector(paginationOptions.nextArrowSelector)
    : null;

  const waitForSwiper = setInterval(() => {
    if (swiperEl.swiper) {
      clearInterval(waitForSwiper);
      const swiperInstance = swiperEl.swiper;

      const slideCount = swiperInstance.slides.length;
      const dotCount = Math.max(0, slideCount); // Bỏ slide đầu và cuối
      let dots = [];

      if (paginationContainer) {
        // Xóa các dot cũ nhưng giữ lại prev/next arrow nếu có
        paginationContainer.querySelectorAll('.dot').forEach(dot => dot.remove());

        if (prevArrow) paginationContainer.appendChild(prevArrow);

        for (let i = 0; i < dotCount; i++) {
          const dot = document.createElement('span');
          dot.classList.add('dot');
          dot.setAttribute('data-index', i ); // dot tương ứng slide i+1
          paginationContainer.appendChild(dot);
          dots.push(dot);

          dot.addEventListener('click', () => {
            swiperInstance.slideTo(i + 1);
          });
        }

        if (nextArrow) paginationContainer.appendChild(nextArrow);
      }

      const updateDots = () => {
        if (!dots || !swiperInstance) return;
        const activeIndex = swiperInstance.realIndex ?? swiperInstance.activeIndex;
        const dotIndex = activeIndex ;

        dots.forEach(dot => dot.classList.remove('active'));
        if (dotIndex >= 0 && dotIndex < dots.length) {
          dots[dotIndex].classList.add('active');
        }
      };

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
initSwiper('.mySwiper', {
  paginationContainerSelector: '.highlighted-projects .custom-pagination',
  prevArrowSelector: '.highlighted-projects .arrow.prev',
  nextArrowSelector: '.highlighted-projects .arrow.next'
});

initSwiper('.mySwiper2', {
  paginationContainerSelector: '.feedback-news-section .custom-pagination',
  prevArrowSelector: '.feedback-news-section .arrow.prev',
  nextArrowSelector: '.feedback-news-section .arrow.next'
});

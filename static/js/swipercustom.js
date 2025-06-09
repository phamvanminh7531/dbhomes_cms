// Khởi tạo và quản lý swiper thứ nhất
// Hàm khởi tạo và quản lý Swiper
function initSwiper(swiperSelector, paginationOptions = {}) {
  const swiperEl = document.querySelector(swiperSelector);
  const dots = paginationOptions.dotsSelector ? document.querySelectorAll(paginationOptions.dotsSelector) : null;
  const prevArrow = paginationOptions.prevArrowSelector ? document.querySelector(paginationOptions.prevArrowSelector) : null;
  const nextArrow = paginationOptions.nextArrowSelector ? document.querySelector(paginationOptions.nextArrowSelector) : null;

  // Hàm cập nhật dots
  const updateDots = () => {
    if (!swiperEl.swiper || !dots) return;
    const activeIndex = swiperEl.swiper.realIndex ?? swiperEl.swiper.activeIndex;
    
    dots.forEach(dot => dot.classList.remove('active'));
    if (dots[activeIndex]) dots[activeIndex].classList.add('active');
  };

  // Chờ swiper khởi tạo
  const waitForSwiper = setInterval(() => {
    if (swiperEl.swiper) {
      clearInterval(waitForSwiper);
      const swiperInstance = swiperEl.swiper;

      // Xử lý dots nếu có
      if (dots && dots.length > 0) {
        dots.forEach((dot, index) => {
          dot.addEventListener('click', () => {
            swiperInstance.slideTo(index);
          });
        });
      }

      // Xử lý prev arrow nếu có
      if (prevArrow) {
        prevArrow.addEventListener('click', () => {
          if (!swiperInstance.isBeginning) {
            swiperInstance.slidePrev();
          }
        });
      }

      // Xử lý next arrow nếu có
      if (nextArrow) {
        nextArrow.addEventListener('click', () => {
          if (!swiperInstance.isEnd) {
            swiperInstance.slideNext();
          }
        });
      }

      // Cập nhật dots khi slide thay đổi
      swiperInstance.on('slideChange', updateDots);
      
      // Cập nhật dots ban đầu
      updateDots();
    }
  }, 100);
}

// Khởi tạo swiper dự án nổi bật
initSwiper('.mySwiper', {
  dotsSelector: '.highlighted-projects .dot',
  prevArrowSelector: '.highlighted-projects .arrow.prev',
  nextArrowSelector: '.highlighted-projects .arrow.next'
});

// Khởi tạo swiper phản hồi khách hàng
initSwiper('.mySwiper2', {
  dotsSelector: '.feedback-news-section .dot',
  prevArrowSelector: '.feedback-news-section .arrow.prev',
  nextArrowSelector: '.feedback-news-section .arrow.next'
});
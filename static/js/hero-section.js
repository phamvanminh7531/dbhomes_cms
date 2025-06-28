window.addEventListener('DOMContentLoaded', () => {
  AOS.init({
    once: false, // 👈 mặc định cho toàn trang: chạy lại mỗi lần cuộn tới
    duration: 1000,
    easing: 'ease-out-cubic',
  });

  setTimeout(() => {
    const title = document.getElementById('main-title');
    if (title) {
      title.classList.add('active');
    }
  }, 1200);
});

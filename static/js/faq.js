document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', () => {
      const faqItem = question.parentElement;
      const isActive = faqItem.classList.contains('active');

      // Đóng tất cả các mục
      document.querySelectorAll('.faq-item.active').forEach(item => {
        item.classList.remove('active');
        item.querySelector('.faq-toggle').textContent = '+';
      });

      // Nếu mục hiện tại chưa active thì bật nó lên
      if (!isActive) {
        faqItem.classList.add('active');
        question.querySelector('.faq-toggle').textContent = '−';
      }
    });
  });
});

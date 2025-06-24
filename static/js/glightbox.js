// Tải GLightbox JS trước khi init (dùng dynamic import)

function loadGlightboxScript(callback) {
  const script = document.createElement('script');
  script.src = 'https://cdn.jsdelivr.net/npm/glightbox/dist/js/glightbox.min.js';
  script.onload = callback;
  document.head.appendChild(script);
}

document.addEventListener('DOMContentLoaded', function () {
  // Load GLightbox trước khi sử dụng
  loadGlightboxScript(function () {
    document.querySelectorAll('.project-detail__main img').forEach(function(img) {
      img.classList.add('glightbox');
      // Không cần thêm data-title, GLightbox sẽ tự lấy alt làm title
    });

    const lightbox = GLightbox({
      selector: '.glightbox'
    });
  });
});
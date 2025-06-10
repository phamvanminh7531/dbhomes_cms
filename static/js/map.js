document.addEventListener('DOMContentLoaded', function () {
  const officeBoxes = document.querySelectorAll('.showroom-section__office-box');
  const iframe = document.querySelector('.showroom-section__map iframe');

  officeBoxes.forEach(box => {
    box.addEventListener('click', () => {
      // Bỏ class 'active' khỏi tất cả box
      officeBoxes.forEach(b => b.classList.remove('active'));

      // Thêm class 'active' vào box được click
      box.classList.add('active');

      // Đổi src cho iframe dựa trên data-map
      const mapUrl = box.getAttribute('data-map');
      if (mapUrl) {
        iframe.setAttribute('src', mapUrl);
      }
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const paginationContainer = document.querySelector('.projects-section__pagination');
  const paginationLinks = paginationContainer.querySelectorAll('a');

  // paginationLinks.forEach((link, index) => {
  //   if (!link.classList.contains('projects-section__arrow')) {
  //     link.addEventListener('click', function (event) {
  //       event.preventDefault();
  //       setActiveLink(this);
  //       updateVisibleItems(index);
  //       setTimeout(equalizeHeights, 0); // Đợi DOM update xong rồi tính lại height
  //     });
  //   } else {
  //     link.addEventListener('click', function (event) {
  //       event.preventDefault();
  //       handleArrowClick(this);
  //       setTimeout(equalizeHeights, 0);
  //     });
  //   }
  // });

  // function setActiveLink(link) {
  //   const current = paginationContainer.querySelector('a.active');
  //   if (current) current.classList.remove('active');
  //   link.classList.add('active');
  // }

  // function handleArrowClick(arrow) {
  //   const current = paginationContainer.querySelector('a.active');
  //   if (!current) return;

  //   const links = Array.from(paginationContainer.querySelectorAll('a'))
  //     .filter(a => !a.classList.contains('projects-section__arrow'));

  //   const currentIndex = links.indexOf(current);

  //   if (arrow.textContent.trim() === '<' && currentIndex > 0) {
  //     setActiveLink(links[currentIndex - 1]);
  //     updateVisibleItems(currentIndex - 1);
  //   }

  //   if (arrow.textContent.trim() === '>' && currentIndex < links.length - 1) {
  //     setActiveLink(links[currentIndex + 1]);
  //     updateVisibleItems(currentIndex + 1);
  //   }
  // }

  function updateVisibleItems(pageIndex) {
    const itemsPerPage = 9; // Tuỳ bạn, ví dụ mỗi trang 9 item
    const items = document.querySelectorAll('.projects-section__item');
    items.forEach((item, i) => {
      if (i >= pageIndex * itemsPerPage && i < (pageIndex + 1) * itemsPerPage) {
        item.style.display = 'block';
      } else {
        item.style.display = 'none';
      }
    });
  }

  function equalizeHeights() {
    const itemsPerRow = 3;
    const items = Array.from(document.querySelectorAll('.projects-section__item'))
      .filter(item => item.style.display !== 'none');  // chỉ tính các item đang hiển thị

    // Reset height
    ['.projects-section__title', '.projects-section__desc', '.projects-section__link'].forEach(selector => {
      items.forEach(item => {
        const el = item.querySelector(selector);
        if (el) el.style.height = 'auto';
      });
    });

    for (let i = 0; i < items.length; i += itemsPerRow) {
      const rowItems = items.slice(i, i + itemsPerRow);
      
      ['.projects-section__title', '.projects-section__desc', '.projects-section__link'].forEach(selector => {
        let maxHeight = 0;
        rowItems.forEach(item => {
          const el = item.querySelector(selector);
          if (el) {
            const height = el.offsetHeight;
            if (height > maxHeight) maxHeight = height;
          }
        });
        rowItems.forEach(item => {
          const el = item.querySelector(selector);
          if (el) {
            el.style.height = maxHeight + 'px';
          }
        });
      });
    }
  }

  // Khởi tạo lần đầu khi trang load
  updateVisibleItems(0);
  setTimeout(equalizeHeights, 0);
  
  // Chạy lại khi resize
  window.addEventListener('resize', () => setTimeout(equalizeHeights, 0));
});

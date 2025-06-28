document.addEventListener("DOMContentLoaded", function () {
  const imageWrappers = document.querySelectorAll(".product-section__item__image-wrapper");
  const breadcrumbCurrent = document.getElementById("breadcrumb-current");
  const breadcrumbSeparator = document.getElementById("breadcrumb-separator");

  imageWrappers.forEach(wrapper => {
    wrapper.addEventListener("click", function () {
      // Xoá class active khỏi tất cả image-wrapper
      imageWrappers.forEach(w => w.classList.remove("active"));

      // Thêm class active vào image-wrapper được click
      wrapper.classList.add("active");

      // Truy ngược lên thẻ .product-section__item để lấy <p>
      const parentItem = wrapper.closest(".product-section__item");
      const productName = parentItem.querySelector("p").textContent;

      // Hiển thị breadcrumb
      breadcrumbCurrent.textContent = productName;
      breadcrumbCurrent.style.display = "inline";
      breadcrumbSeparator.style.display = "inline";
    });
  });
});

// document.addEventListener("DOMContentLoaded", () => {
//   const slider = document.querySelector(".product-section__slider");
//   const slides = document.querySelectorAll(".product-section__grid");
//   const prevBtn = document.getElementById("prev-btn");
//   const nextBtn = document.getElementById("next-btn");

//   let currentIndex = 0;

//   const updateSliderPosition = () => {
//     const offset = -currentIndex * 100;
//     slider.style.transform = `translateX(${offset}%)`;
//   };

//   prevBtn.addEventListener("click", () => {
//     if (currentIndex > 0) {
//       currentIndex--;
//       updateSliderPosition();
//     }
//   });

//   nextBtn.addEventListener("click", () => {
//     if (currentIndex < slides.length - 1) {
//       currentIndex++;
//       updateSliderPosition();
//     }
//   });

//   updateSliderPosition(); // Khởi tạo vị trí ban đầu
// });
// product-slider.js
function getItemsPerPage() {
  const screenWidth = window.innerWidth;

  if (screenWidth <= 624) return 1; // Mobile layout: 1 item per view
  if (screenWidth <= 921) return 4; // 2 columns × 2 rows
  if (screenWidth <= 1148) return 6; // 3 columns × 2 rows

  return 8; // Default: 4 columns × 2 rows
}
const itemsPerPage = getItemsPerPage();
let currentPage = 0;

function updateSlider() {
  const items = document.querySelectorAll('.product-section__item');
  const itemsPerPage = getItemsPerPage(); 
  items.forEach(item => {
    item.classList.remove('show', 'fade-in');
  });

  setTimeout(() => {
    let visibleCount = 0;
    items.forEach((item, index) => {
      if (index >= currentPage * itemsPerPage && index < (currentPage + 1) * itemsPerPage) {
        item.classList.add('show', 'fade-in');
        visibleCount++;
      }
    });

    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');

    // Thiết lập top phù hợp với layout hiện tại
    let topValue;
    switch (itemsPerPage) {
      case 1: // mobile
        topValue = '49%';
        break;
      case 4: // 2x2 layout
        topValue = '47.5%';
        break;
      case 6: // 3x2 layout
      case 8: // 4x2 layout
      default:
        topValue = '47%';
        break;
    }

    prevBtn.style.top = topValue;
    nextBtn.style.top = topValue;
  }, 100);
}


function slideLeft() {
  if (currentPage > 0) {
    currentPage--;
    updateSlider();
  }
}

function slideRight() {
  const items = document.querySelectorAll('.product-section__item');
    const itemsPerPage = getItemsPerPage(); 
  const maxPage = Math.floor((items.length - 1) / itemsPerPage);
  if (currentPage < maxPage) {
    currentPage++;
    updateSlider();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  updateSlider();
  document.getElementById('prev-btn').addEventListener('click', slideLeft);
  document.getElementById('next-btn').addEventListener('click', slideRight);
});

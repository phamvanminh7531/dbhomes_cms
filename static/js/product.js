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

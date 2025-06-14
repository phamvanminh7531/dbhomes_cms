document.addEventListener("DOMContentLoaded", function () {
  const tabButtons = document.querySelectorAll(".tab-menu .tab");

  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      // Bỏ class 'active' khỏi tất cả các nút
      tabButtons.forEach((btn) => btn.classList.remove("active"));

      // Thêm class 'active' vào nút được click
      button.classList.add("active");
    });
  });
});

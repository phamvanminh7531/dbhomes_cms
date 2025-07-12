document.addEventListener("DOMContentLoaded", () => {
  const iconClasses = [
    "fa-solid fa-phone",
    "fab fa-facebook-messenger",
  ];
  let current = 0;
  let menuOpen = false;

  const rotatingIcon = document.querySelector("#toggleMenu i");
  const toggleBtn = document.getElementById("toggleMenu");
  const menu = document.getElementById("contactMenu");
  const menuItems = document.querySelectorAll(".menu-item");

  // Auto icon rotation
  setInterval(() => {
    if (!menuOpen) {
      rotatingIcon.className = iconClasses[current];
      rotatingIcon.style.color = "white";
      current = (current + 1) % iconClasses.length;
    }
  }, 2000);

  // Toggle menu
  toggleBtn.addEventListener("click", () => {
    menuOpen = !menuOpen;
    menu.style.display = menuOpen ? "flex" : "none";

    menuItems.forEach((item, index) => {
      const defaultIcon = item.querySelector(".icon-default");
      const svgIcon = item.querySelector(".icon-svg");

      if (menuOpen) {
        // Hiện SVG, ẩn icon font
        if (defaultIcon) defaultIcon.style.display = "none";
        if (svgIcon) {
          svgIcon.style.display = "inline-flex";
          svgIcon.classList.add("icon-wrapper", `bg-${index}`);
        }
      } else {
        // Hiện icon font, ẩn SVG
        if (defaultIcon) defaultIcon.style.display = "inline-flex";
        if (svgIcon) {
          svgIcon.style.display = "none";
          svgIcon.classList.remove("icon-wrapper", `bg-${index}`);
        }
      }
    });
  });
});

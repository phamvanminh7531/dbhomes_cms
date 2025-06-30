document.addEventListener("DOMContentLoaded", () => {
  const grid = document.querySelector(".core-values-grid");
  const items = grid.querySelectorAll(".core-value-item");

  if (items.length === 5) {
    grid.classList.add("five-items");
  } else {
    grid.classList.remove("five-items");
  }
});

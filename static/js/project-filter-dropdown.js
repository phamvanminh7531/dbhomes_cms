document.addEventListener("DOMContentLoaded", function () {
  const dropdowns = document.querySelectorAll(".dropdown");
  const tagContainer = document.getElementById("filter-tags-container");

  dropdowns.forEach((dropdown, index) => {
    const button = dropdown.querySelector(".dropdown-toggle");
    const menuItems = dropdown.querySelectorAll(".dropdown-menu li");
    const tagId = `filter-tag-${index}`; // Unique tag per dropdown

    // Toggle dropdown
    button.addEventListener("click", function (e) {
      e.stopPropagation();

      dropdowns.forEach(d => {
        if (d !== dropdown) {
          d.classList.remove("open");
          d.querySelector(".dropdown-toggle")?.classList.remove("filter-button--active");
        }
      });

      dropdown.classList.toggle("open");
      button.classList.toggle("filter-button--active");
    });

    // Handle item click
    menuItems.forEach(item => {
      item.addEventListener("click", function (e) {
        e.stopPropagation();
        const value = item.textContent.trim();

        // Remove existing tag if any
        const oldTag = document.getElementById(tagId);
        if (oldTag) oldTag.remove();

        // Create new tag
        const tag = document.createElement("div");
        tag.className = "filter-tag";
        tag.id = tagId;
        tag.textContent = `x ${value}`;

        // Add click to remove itself
        tag.addEventListener("click", function () {
          tag.remove();
        });

        tagContainer.appendChild(tag);

        // Close dropdown
        dropdown.classList.remove("open");
        button.classList.remove("filter-button--active");
      });
    });
  });

  // Close dropdowns when clicking outside
  document.addEventListener("click", function () {
    dropdowns.forEach(d => {
      d.classList.remove("open");
      d.querySelector(".dropdown-toggle")?.classList.remove("filter-button--active");
    });
  });
});

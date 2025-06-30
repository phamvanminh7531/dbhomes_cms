document.addEventListener("DOMContentLoaded", function () {
  const wrapper = document.querySelector(".consultation-section .custom-select-wrapper");
  if (!wrapper) return;

  const trigger = wrapper.querySelector(".custom-select-trigger");
  const dropdown = wrapper.querySelector(".custom-select-dropdown");
  const list = wrapper.querySelector("#provinceList2");
  const input = wrapper.querySelector("#provinceSearchInput2");
  const hiddenInput = wrapper.querySelector("#provinceSelectHidden2");

  let allProvinces = [];

  fetch('https://provinces.open-api.vn/api/?depth=1')
    .then(res => res.json())
    .then(data => {
      allProvinces = data.map(p => ({
        name: p.name,
        displayName: p.name,
        searchName: removeVietnamese(p.name.replace(/^Tỉnh |^Thành phố /i, '').toLowerCase())
      }));
      renderList(allProvinces);
    });

  function renderList(provinces) {
    list.innerHTML = "";
    provinces.forEach(p => {
      const li = document.createElement("li");
      li.textContent = p.displayName;
      li.addEventListener("mousedown", () => {
        trigger.textContent = p.displayName;
        hiddenInput.value = p.displayName;
        dropdown.style.display = "none";
      });
      list.appendChild(li);
    });
  }

  function removeVietnamese(str) {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/đ/g, "d").replace(/Đ/g, "D");
  }

  input.addEventListener("input", function () {
    const keyword = removeVietnamese(this.value.toLowerCase());
    const filtered = allProvinces.filter(p => p.searchName.includes(keyword));
    renderList(filtered);
  });

  trigger.addEventListener("click", function (e) {
    e.stopPropagation();
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
    input.value = "";
    renderList(allProvinces);
    setTimeout(() => input.focus(), 10);
  });

  // ✅ Chỉ đóng dropdown trong consultation-section nếu click ra ngoài
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".consultation-section .custom-select-wrapper")) {
      dropdown.style.display = "none";
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const select = document.getElementById("requirementSelect2");
  const otherInput = document.getElementById("otherInput2");

  select.addEventListener("change", function () {
    if (this.value === "Khác") {
      otherInput.style.display = "block";
      otherInput.required = true;
      otherInput.style.backgroundColor="transparent"
      otherInput.style.color="rgba(67, 35, 12, 0.6)"
    } else {
      otherInput.style.display = "none";
      otherInput.required = false;
      otherInput.value = "";
    }
  });
});

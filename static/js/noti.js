document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("successModal");
  const closeModalBtn = document.getElementById("closeModalBtn");

  const consultationForm = document.getElementById("consultationForm");

  function handleFormSubmit(form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      const formData = new FormData(form);

      fetch(form.action, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest", // Để phân biệt Ajax
        },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            form.reset();
            modal.style.display = "flex";
          } else {
            alert(data.error || "Đã có lỗi xảy ra.");
          }
        })
        .catch((error) => {
          console.error("Lỗi gửi form:", error);
          alert("Lỗi kết nối. Vui lòng thử lại sau.");
        });
    });
  }

  if (consultationForm) {
    handleFormSubmit(consultationForm);
  }

  closeModalBtn.addEventListener("click", function () {
    modal.style.display = "none";
  });

  window.addEventListener("click", function (e) {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});

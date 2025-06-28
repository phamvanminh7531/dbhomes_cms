document.addEventListener("DOMContentLoaded", function () {
  const track = document.querySelector(".dbverse-section .main-content-container .container");
  const slides = track.querySelectorAll(".dbverse-block");
  const prevBtn = document.getElementById("prev-slide");
  const nextBtn = document.getElementById("next-slide");

  let currentSlide = 0;
  const totalSlides = slides.length;

  function updateSlidePosition() {
    track.style.transform = `translateX(-${currentSlide * 100}%)`;
  }

  // Nút chuyển slide
  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
      updateSlidePosition();
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      currentSlide = (currentSlide + 1) % totalSlides;
      updateSlidePosition();
    });
  }

  // Auto slide every 6 seconds
  setInterval(() => {
    currentSlide = (currentSlide + 1) % totalSlides;
    updateSlidePosition();
  }, 6000);

  // --- Swipe (touch) ---
  let startX = 0;
  let endX = 0;

  track.addEventListener("touchstart", (e) => {
    startX = e.touches[0].clientX;
  });

  track.addEventListener("touchmove", (e) => {
    endX = e.touches[0].clientX;
  });

  track.addEventListener("touchend", () => {
    const threshold = 50;
    if (startX - endX > threshold) {
      currentSlide = (currentSlide + 1) % totalSlides;
      updateSlidePosition();
    } else if (endX - startX > threshold) {
      currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
      updateSlidePosition();
    }
    startX = 0;
    endX = 0;
  });

  // --- Drag (mouse) ---
  let isDragging = false;
  let dragStartX = 0;
  let dragEndX = 0;

  track.addEventListener("mousedown", (e) => {
    isDragging = true;
    dragStartX = e.clientX;
    track.style.cursor = "grabbing";
  });

  track.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    dragEndX = e.clientX;
  });

  track.addEventListener("mouseup", () => {
    if (!isDragging) return;
    const threshold = 50;
    if (dragStartX - dragEndX > threshold) {
      currentSlide = (currentSlide + 1) % totalSlides;
      updateSlidePosition();
    } else if (dragEndX - dragStartX > threshold) {
      currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
      updateSlidePosition();
    }
    isDragging = false;
    dragStartX = 0;
    dragEndX = 0;
    track.style.cursor = "grab";
  });

  track.addEventListener("mouseleave", () => {
    isDragging = false;
    track.style.cursor = "grab";
  });

  // Giao diện chuột mặc định
  track.style.cursor = "grab";
});

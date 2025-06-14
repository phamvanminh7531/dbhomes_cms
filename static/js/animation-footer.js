document.addEventListener("DOMContentLoaded", () => {
  const waitForFooter = setInterval(() => {
    const footer = document.querySelector(".footer-db");

    if (footer) {
      clearInterval(waitForFooter); // ngừng kiểm tra
      const observer = new IntersectionObserver(
        (entries, obs) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              footer.classList.add("footer-in-view");
              obs.unobserve(entry.target);
            }
          });
        },
        {
          threshold: 0.2,
        }
      );

      observer.observe(footer);
    }
  }, 100); // kiểm tra mỗi 100ms
});

const scrollBtn = document.getElementById("scrollToTopBtn");

window.addEventListener("scroll", () => {
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const scrollPercent = (scrollTop / docHeight) * 100;

  scrollBtn.style.display = scrollTop > 100 ? "flex" : "none";
  scrollBtn.style.setProperty('--scroll', `${scrollPercent}%`);
});

scrollBtn.addEventListener("click", () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });
});

imagesLoaded(document.body, { background: true }, function () {
  const loadingScreen = document.getElementById("loading-screen");
  if (!loadingScreen) return;

  loadingScreen.style.transition = "opacity 0.5s ease";
  loadingScreen.style.opacity = "0";

  setTimeout(() => loadingScreen.remove(), 500);
});

document.addEventListener('DOMContentLoaded', function () {
  const paginationContainer = document.querySelector('.projects-section__pagination');
  const paginationLinks = paginationContainer.querySelectorAll('a');

  paginationLinks.forEach((link, index) => {
    if (!link.classList.contains('projects-section__arrow')) {
      link.addEventListener('click', function (event) {
        event.preventDefault();
        setActiveLink(this);
      });
    } else {
      link.addEventListener('click', function (event) {
        event.preventDefault();
        handleArrowClick(this);
      });
    }
  });

  function setActiveLink(link) {
    const current = paginationContainer.querySelector('a.active');
    if (current) current.classList.remove('active');
    link.classList.add('active');
  }

  function handleArrowClick(arrow) {
    const current = paginationContainer.querySelector('a.active');
    if (!current) return;

    const links = Array.from(paginationContainer.querySelectorAll('a'))
      .filter(a => !a.classList.contains('projects-section__arrow'));

    const currentIndex = links.indexOf(current);

    if (arrow.textContent.trim() === '<' && currentIndex > 0) {
      setActiveLink(links[currentIndex - 1]);
    }

    if (arrow.textContent.trim() === '>' && currentIndex < links.length - 1) {
      setActiveLink(links[currentIndex + 1]);
    }
  }
});

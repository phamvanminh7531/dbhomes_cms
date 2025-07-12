document.addEventListener("DOMContentLoaded", function () {
    // Initialize Tocbot
    tocbot.init({
        tocSelector: '#toc',
        contentSelector: '#content',
        headingSelector: 'h1, h2, h3, h4, h5',
        ignoreSelector: '.js-toc-ignore',
        hasInnerContainers: true,
        collapseDepth: 6,
        scrollSmooth: true,
        scrollSmoothDuration: 400,
        scrollSmoothOffset: -80,
        fixedSidebarOffset: 'auto',
        includeHtml: false,
        orderedList: true, // Show numbered list
        listItemClass: 'toc-list-item',
        listClass: 'toc-list',
        linkClass: 'toc-link',
        activeListItemClass: 'is-active-li',
        activeLinkClass: 'is-active-link',
    });

    // Toggle show/hide TOC
  window.toggleTOC = function () {
    const toc = document.getElementById('toc');
    const container = document.querySelector('.toc-container');
    const isShown = toc.classList.toggle('show');

    if (isShown) {
        container.classList.add('open');
        container.classList.remove('closed');
    } else {
        container.classList.add('closed');
        container.classList.remove('open');
    }
};


    // Optional: Watch for content changes (e.g., in dynamic SPA or AJAX)
    const observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            if (mutation.type === 'childList') {
                tocbot.refresh();
            }
        });
    });

    const content = document.getElementById('content');
    if (content) {
        observer.observe(content, {
            childList: true,
            subtree: true
        });
    }
});

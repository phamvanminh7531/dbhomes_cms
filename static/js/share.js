document.addEventListener('DOMContentLoaded', function () {
  const toast = document.createElement('div');
  toast.className = 'toast';
  document.body.appendChild(toast);

  const facebookBtn = document.getElementById('facebook-share');
  const copyBtn = document.getElementById('copy-share');

  if (facebookBtn) {
    facebookBtn.style.cursor = 'pointer';
    facebookBtn.addEventListener('click', function () {
      const currentUrl = encodeURIComponent(window.location.href);
      const facebookShareUrl = `https://www.facebook.com/sharer/sharer.php?u=${currentUrl}`;
      window.open(facebookShareUrl, '_blank', 'width=600,height=400');
    });
  }

  if (copyBtn) {
    copyBtn.style.cursor = 'pointer';
    copyBtn.addEventListener('click', function () {
      const currentUrl = window.location.href;

      if (typeof navigator.clipboard !== 'undefined') {
        if (typeof navigator.clipboard.writeText === 'function') {
          navigator.clipboard.writeText(currentUrl)
            .then(() => {
              showToast('Link copied to clipboard!');
            })
            .catch(err => {
              console.error('Error copying link: ', err);
              fallbackCopy(currentUrl);
            });
        } else {
          fallbackCopy(currentUrl);
        }
      } else {
        fallbackCopy(currentUrl);
      }
    });
  }

  function fallbackCopy(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    try {
      const successful = document.execCommand('copy');
      if (successful) {
        showToast('Link copied to clipboard!');
      } else {
        showToast('Failed to copy!');
      }
    } catch (err) {
      console.error('Fallback error:', err);
      showToast('Copy failed!');
    }
    document.body.removeChild(textArea);
  }

  function showToast(message) {
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 2500);
  }
});

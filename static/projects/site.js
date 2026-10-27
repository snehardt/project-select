// Native <details> works without JavaScript; this links directly into the gallery.
document.querySelectorAll('[data-open-gallery]').forEach((link) => {
  link.addEventListener('click', () => {
    const gallery = document.getElementById('screenshots');
    if (gallery) gallery.open = true;
  });
});
if (window.location.hash === '#screenshots') {
  const gallery = document.getElementById('screenshots');
  if (gallery) gallery.open = true;
}

// menu.js
document.addEventListener('DOMContentLoaded', function () {
  const menuButton = document.querySelector('[aria-controls="mobile-menu"]');
  const mobileMenu = document.getElementById('mobile-menu');

  if (menuButton && mobileMenu) {
    const menuIcon = menuButton.querySelector('svg:nth-child(1)');
    const closeIcon = menuButton.querySelector('svg:nth-child(2)');

    menuButton.addEventListener('click', function () {
      const expanded = this.getAttribute('aria-expanded') === 'true' || false;
      this.setAttribute('aria-expanded', !expanded);
      mobileMenu.classList.toggle('hidden');
      menuIcon.classList.toggle('hidden');
      closeIcon.classList.toggle('hidden');
    });

    // Cerrar el menú al hacer clic fuera de él
    document.addEventListener('click', function (event) {
      const isClickInside =
        mobileMenu.contains(event.target) || menuButton.contains(event.target);
      if (!isClickInside && !mobileMenu.classList.contains('hidden')) {
        menuButton.setAttribute('aria-expanded', 'false');
        mobileMenu.classList.add('hidden');
        menuIcon.classList.remove('hidden');
        closeIcon.classList.add('hidden');
      }
    });
  } else {
    console.warn('Menu button or mobile menu not found');
  }
});

document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('nav ul');

    // Mobile menu toggle
    menuToggle.addEventListener('click', () => {
        nav.classList.toggle('active');
    });

    // Sticky Navbar
    const header = document.querySelector('header');
    const stickyOffset = header.offsetTop; // Get the offset top of the navbar

    function makeSticky() {
        if (window.pageYOffset > stickyOffset) {
            header.classList.add('sticky'); // Add sticky class when you scroll past the navbar
        } else {
            header.classList.remove('sticky'); // Remove sticky class when you are at the top of the page
        }
    }

    window.addEventListener('scroll', makeSticky);
});

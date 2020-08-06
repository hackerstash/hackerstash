const hamburger = document.querySelector('.hamburger');

const openHamburgerIcon = 'ri-menu-line';
const closeHamburgerIcon = 'ri-close-line';

if (hamburger) {
    hamburger.addEventListener('click', (event) => {
        const element = event.target;

        element.classList.toggle(openHamburgerIcon);
        element.classList.toggle(closeHamburgerIcon);

        document.getElementById('sidebar').classList.toggle('menu-open');
    });
}
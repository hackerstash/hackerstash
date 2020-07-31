var hamburger = document.querySelector('.hamburger');

var openHamburgerIcon = 'ri-menu-line';
var closeHamburgerIcon = 'ri-close-line';

if (hamburger) {
    hamburger.addEventListener('click', function(event) {
        var element = event.target;

        element.classList.toggle(openHamburgerIcon);
        element.classList.toggle(closeHamburgerIcon);

        document.getElementById('sidebar').classList.toggle('menu-open');
    });
}
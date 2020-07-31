var file = document.getElementById('file');
var avatar = document.getElementById('avatar');
var deleteAvatarButton = document.querySelector('.delete-avatar');

if (file) {
    file.addEventListener('change', function(event) {
        var file = event.target.files[0];
        var container = document.querySelector('.edit-avatar');
        var icon = container.querySelector('.avatar');

        var img = document.createElement('img');
        img.src = URL.createObjectURL(file);

        icon.innerHTML = '';
        icon.appendChild(img);
        container.classList.remove('no-image');
    });
}

if (deleteAvatarButton) {
    deleteAvatarButton.addEventListener('click', function () {
        var container = document.querySelector('.edit-avatar');
        var icon = container.querySelector('.avatar');
        icon.innerHTML = '<span class="placeholder">$</span>';
        container.classList.add('no-image');
        file.value = '';
        avatar.value = '';
    });
}
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
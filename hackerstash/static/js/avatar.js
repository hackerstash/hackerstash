var file = document.getElementById('file');
var avatar = document.getElementById('avatar');
var deleteAvatarButton = document.querySelector('.delete-avatar');

if (file) {
    file.addEventListener('change', function(event) {
        var file = event.target.files[0];
        var container = document.querySelector('.edit-avatar');

        // There are multiple image uploads, if the
        // avatar container is not available it's likely
        // something else (e.g. posts)
        if (!container) return null;

        var icon = container.querySelector('.avatar');
        var img = document.createElement('img');
        img.src = URL.createObjectURL(file);

        icon.innerHTML = '';
        icon.appendChild(img);
        container.classList.remove('no-image');
    });
}

if (deleteAvatarButton) {
    deleteAvatarButton.addEventListener('click', function() {
        var container = document.querySelector('.edit-avatar');
        var icon = container.querySelector('.avatar');
        icon.innerHTML = '<span class="placeholder">$</span>';
        container.classList.add('no-image');
        file.value = '';
        avatar.value = '';
    });
}
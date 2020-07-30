var avatar = document.getElementById('avatar');
var deleteAvatarButton = document.querySelector('.delete-avatar');

if (avatar) {
    avatar.addEventListener('change', function(event) {
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
        icon.innerHTML = '<p>$</p>';
        container.classList.add('no-image');
        avatar.value = '';
    });
}
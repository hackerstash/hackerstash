const avatarFile = document.getElementById('file');
const avatar = document.getElementById('avatar');
const deleteAvatarButton = document.querySelector('.delete-avatar');

if (avatarFile) {
    avatarFile.addEventListener('change', (event) => {
        const image = event.target.files[0];
        const container = document.querySelector('.edit-avatar');

        // There are multiple image uploads, if the
        // avatar container is not available it's likely
        // something else (e.g. posts)
        if (!container) return null;

        const icon = container.querySelector('.avatar');
        const img = document.createElement('img');
        img.src = URL.createObjectURL(image);

        icon.innerHTML = '';
        icon.appendChild(img);
        container.classList.remove('no-image');
    });
}

if (deleteAvatarButton) {
    deleteAvatarButton.addEventListener('click', () => {
        const container = document.querySelector('.edit-avatar');
        const icon = container.querySelector('.avatar');
        icon.innerHTML = '<span class="placeholder">$</span>';
        container.classList.add('no-image');
        avatarFile.value = '';
        avatar.value = '';
    });
}
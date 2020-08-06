const postFile = document.getElementById('file');
const body = document.getElementById('body');

if (postFile) {
    postFile.addEventListener('change', (event) => {
        const files = event.target.files;
        const container = document.querySelector('.post-images');

        // If the container doesn't exist then it's
        // likely something else (e.g. avatars)
        if (!container) return;

        Array.from(files).forEach((file) => {
            const img = document.createElement('img');
            const imgContainer = document.createElement('div');
            const list = document.createElement('li');
            const button = document.createElement('button');

            // Set up the image
            img.src = URL.createObjectURL(file);

            // Set up the image container
            imgContainer.classList.add('image');
            imgContainer.appendChild(img);

            // Set up the close button
            button.classList.add('button', 'link', 'delete-image');
            button.setAttribute('type', 'button');
            button.setAttribute('data-file-name', file.name);
            button.innerHTML = '<i class="icon ri-close-line"></i>';

            // Set up the list item
            list.appendChild(imgContainer);
            list.appendChild(button);

            container.appendChild(list);
            body.value += '![Alt text](' + file.name + ')\n';

            // You can't remove items from input[type=file] as the FileList
            // is read only. Keep a record of file names to upload as the
            // user may remove some
            const fileNameInput = document.getElementById('filenames_to_upload');
            const fileNames = JSON.parse(fileNameInput.value);
            fileNames.push(file.name);
            fileNameInput.value = JSON.stringify(fileNames);
        });
    });
}

document.addEventListener('click', (event) => {
    if (event.target.closest('.delete-image')) {
        const filename = event.target.closest('.delete-image').getAttribute('data-file-name');

        // Delete the thumbnail
        event.target.closest('li').remove();

        const lines = body.value.split('\n');

        // Strip out any references to the file from the textarea
        body.value = lines
            .filter((line) => !line.includes('(' + filename + ')'))
            .join('\n');

        // Remove the filename from the list
        const fileNameInput = document.getElementById('filenames_to_upload');
        const fileNames = JSON.parse(fileNameInput.value);
        fileNames = fileNames.filter((name) => {
            return name !== filename;
        });
        fileNameInput.value = JSON.stringify(fileNames);
    }
});
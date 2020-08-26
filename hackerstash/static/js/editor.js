const editor = document.querySelector('.editor');

function createEditor(selector) {
    const editor = new Quill(selector, {
        modules: {
            toolbar: {
                container: '.toolbar',
                handlers: {
                    image: function() {
                        document.querySelector('.ql-image[type=file]').click();
                    }
                }
            }
        },
    });

    const form = document.querySelector(selector).closest('.editor-form');
    const imageUpload = form.querySelector('.ql-image[type=file]');

    form.addEventListener('submit', event => {
        event.preventDefault();
        event.target.querySelector('.body').value = editor.root.innerHTML;

        // Comments are submitted with fetch so we should not
        // submit here
        if (!event.target.classList.contains('comment-form')) {
            event.target.submit();
        }
    });

    if (imageUpload) {
        imageUpload.addEventListener('change', event => {
            const uploading = document.querySelector('.uploading-images');
            uploading.classList.remove('d-none');

            const form = new FormData();
            Array.from(event.target.files).forEach(file => form.append('file', file));

            const options = {
                credentials: 'include',
                method: 'POST',
                headers: {
                    'x-requested-with': 'fetch',
                },
                body: form
           };

           fetch('/posts/images', options)
               .then((response) => {
                   if (response.ok) {
                       return response.json();
                   }
                   throw new Error(response.statusText);
               })
               .then(keys => {
                   const editor = document.querySelector('.ql-editor');
                   keys.forEach(key => {
                       const img = document.createElement('img');
                       img.src = `https://images.hackerstash.com/${key}`;
                       editor.appendChild(img);
                   });
                   uploading.classList.add('d-none');
               });
        });
    }
}
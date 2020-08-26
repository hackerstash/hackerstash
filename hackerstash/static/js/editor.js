function createEditor(form) {
    const selector = s => document.querySelector(`${form} ${s}`);

    const editor = new Quill(`${form} .editor`, {
        modules: {
            toolbar: {
                container: `${form} .toolbar`,
                handlers: {
                    image: function() {
                        selector('.ql-image[type=file]').click();
                    }
                }
            }
        },
    });

    const imageUpload = selector('.ql-image[type=file]');

    document.querySelector(form).addEventListener('submit', event => {
        event.preventDefault();
        selector('.body').value = editor.root.innerHTML;

        // Comments are submitted with fetch so we should not
        // submit here
        if (!event.target.classList.contains('comment-form')) {
            event.target.submit();
        }
    });

    if (imageUpload) {
        imageUpload.addEventListener('change', event => {
            const uploading = selector('.uploading-images');
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
                   const editor = selector('.ql-editor');
                   keys.forEach(key => {
                       const img = document.createElement('img');
                       img.src = `https://images.hackerstash.com/${key}`;
                       editor.appendChild(img);
                   });
                   uploading.classList.add('d-none');
               });
        });
    }

    return editor;
}
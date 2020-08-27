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

    const headingPicker = selector('.heading-picker');
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

    if (headingPicker) {
        headingPicker.addEventListener('click', event => {
            event.target.closest('.popup-container').querySelector('.popup').classList.toggle('d-none');
        });
    }

    document.addEventListener('click', event => {
        if (event.target.closest('.ql-header')) {
            headingPicker.closest('.popup-container').querySelector('.popup').classList.add('d-none');
        }
    });

    selector('.ql-editor').addEventListener('keyup', event => {
        const input = event.target;
        const text = input.innerText;
        const match = text.match(/@([a-z0-9\_\-\.])+$/);

        closeMentionContainer();

        if (match) {
            const username = match[1].replace('@', '');

            const options = {
                credentials: 'include',
                headers: {
                    'x-requested-with': 'fetch',
                }
            };

            fetch(`/users/usernames?q=${username}`)
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    }
                    throw new Error(response.statusText);
               })
               .then(results => {
                   const mention = document.createElement('div');
                   mention.classList.add('mention-container');
// TODO
//                   results.forEach(result => {
//                       const button = document.createElement('button');
//                       button.classList.add('button');
//                       button.setAttribute('data-username', result.username);
//                       button.innerHTML = `<span>${result.name}</span><span>@${result.username}</span>`;
//                       button.addEventListener('click', event => {
//                           const username = event.target.closest('.button').getAttribute('data-username');
//                           input.innerHTML = input.innerHTML.replace(/@([a-z0-9\_\-\.])+/, `@${username}`);
//                           closeMentionContainer();
//                       });
//                       mention.appendChild(button);
//                   });
//
//                   document.body.appendChild(mention);
               });
        }
    });

    selector('.ql-editor').addEventListener('blur', event => {
        setTimeout(() => {
            closeMentionContainer();
        }, 1000);
    });

    return editor;
}

function closeMentionContainer() {
    const container = document.querySelector('.mention-container');
    if (container) container.remove();
}
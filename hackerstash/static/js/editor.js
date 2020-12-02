function createEditor(container, options = {}) {
    let usernameSearch = '';

    // Create an id so we can localise the quill stuff
    const id = `editor-${Math.random().toString().substr(2, 8)}`;
    const selector = s => container.querySelector(s);

    container.setAttribute('id', id);

    const Link = Quill.import('formats/link');

    class CustomLink extends Link {
        static create(value) {
            const node = super.create(value);
            node.setAttribute('target', '_blank');
            node.setAttribute('rel', 'nofollow noreferrer');
            return node;
        }
    }

    Quill.register(CustomLink);

    const editor = new Quill(`#${id} .editor`, {
        formats: [
            'bold',
            'header',
            'italic',
            'link',
            'underline',
            'strike',
            'code-block',
            'list',
            'blockquote',
            'image',
            'indent',
        ],
        modules: {
            toolbar: {
                container: `#${id} .toolbar`,
                handlers: {
                    image: function() {
                        selector('.ql-image[type=file]').click();
                    }
                }
            }
        },
    });

    if (options.focus) {
        editor.setSelection(99999, 0, 'api');
    }

    if (options.limit) {
        const limit = selector('.editor-limit').getAttribute('data-limit');

        selector('.ql-editor').addEventListener('keyup', event => {
            const max = Number(limit);
            const count = editor.root.innerText.trim().length;

            selector('.editor-limit span').innerText = count;

            if (count > max) {
                selector('.editor-limit').classList.add('error');
            } else {
                selector('.editor-limit').classList.remove('error');
            }
        });
    }

    const headingPicker = selector('.heading-picker');
    const imageUpload = selector('.ql-image[type=file]');

    if (imageUpload) {
        imageUpload.addEventListener('change', event => {
            const files = Array.from(event.target.files);
            if (files.length) {
                setUploadingStart();
                uploadImages(files);
            }
        });
    }

    if (headingPicker) {
        headingPicker.addEventListener('click', event => {
            event.target.closest('.popup-container').querySelector('.popup').classList.toggle('d-none');
        });
    }

    editor.on('editor-change', () => {
        const value = editor.root.innerHTML;
        const length = editor.root.innerText.trim().length;
        selector('input.body').value = length === 0 ? '' : value;
    });

    document.addEventListener('click', event => {
        if (event.target.closest('.ql-header')) {
            headingPicker.closest('.popup-container').querySelector('.popup').classList.add('d-none');
        }
    });

    selector('.ql-editor').addEventListener('keydown', event => {
        if (event.keyCode === 13) {
            event.preventDefault();
            const selected = document.querySelector('.mention-container .selected');

            if (selected) {
                const input = event.target;
                const username = selected.getAttribute('data-username');
                insertUsernameIntoEditor(input, username);
            }
        }
    });

    selector('.ql-editor').addEventListener('keyup', event => {
        const input = event.target;
        const text = input.innerText.trim();
        const match = text.match(/@([a-z0-9\_\-\.])+$/);

        if (!match) {
            return closeMentionContainer();
        }

        const username = match[0].replace('@', '');
        usernameSearch = username;

        const options = {
            credentials: 'include',
            headers: {
                'x-requested-with': 'fetch',
            }
        };

        fetch(`/users/usernames?q=${username}`, options)
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error(response.statusText);
           })
            .then(results => {
                const coords = input.querySelector('p:last-of-type').getBoundingClientRect();

                let mention = document.querySelector('.mention-container');

                if (!mention) {
                    mention = document.createElement('div');
                    mention.classList.add('mention-container');
                    mention.style = `left: ${coords.left}px; top: ${coords.top + coords.height + 8}px`;
                }

                mention.innerHTML = '';

                if (results.length === 0) {
                    return closeMentionContainer();
                }

                results.forEach((result, index) => {
                    const button = document.createElement('button');
                    button.classList.add('button');
                    if (index === 0) button.classList.add('selected');
                    button.setAttribute('data-username', result.username);
                    button.innerHTML = `<span>${result.name}</span><span>@${result.username}</span>`;

                    button.addEventListener('click', event => {
                        const username = event.target.closest('.button').getAttribute('data-username');
                        insertUsernameIntoEditor(input, username);
                    });

                    button.addEventListener('mouseover', event => {
                        event.target.classList.add('selected');
                    });

                    button.addEventListener('mouseout', event => {
                        event.target.classList.remove('selected');
                    });

                    mention.appendChild(button);
                });

                document.body.appendChild(mention);
           });
    });

    selector('.ql-editor').addEventListener('blur', event => {
        // Give it some time for click events to fire
        setTimeout(() => closeMentionContainer(), 100);
    });

    selector('.editor').addEventListener('drop', event => {
        event.preventDefault();

        if (event.dataTransfer.items && !options.light) {
            const files = [];
            setUploadingStart();

            for (let i=0; i<event.dataTransfer.items.length; i++) {
                if (event.dataTransfer.items[i].kind === 'file') {
                    files.push(event.dataTransfer.items[i].getAsFile());
                }
            }

            selector('.editor').classList.remove('dragging');
            uploadImages(files);
        }
    });

    selector('.editor').addEventListener('dragenter', event => {
        if (!options.light) {
            selector('.editor').classList.add('dragging');
        }
    });

    selector('.editor').addEventListener('dragleave', event => {
        if (!options.light) {
            selector('.editor').classList.remove('dragging');
        }
    });

    selector('.ql-editor').addEventListener('paste', event => {
        if (event.clipboardData && !options.light) {
            const files = [];

            for (let i=0; i<event.clipboardData.items.length; i++) {
                if (event.clipboardData.items[i].kind === 'file') {
                    files.push(event.clipboardData.items[i].getAsFile());
                }
            }

            if (files.length) {
                removePastedImage();
                setUploadingStart();
                uploadImages(files);
            }
        }
    });

    function removePastedImage() {
        setTimeout(() => {
            const img = selector('img[src^="data"]');

            if (img) {
                const parent = img.parentElement;

                if (parent.nodeName === 'P') {
                    parent.remove();
                } else {
                    img.remove();
                }
            }
        }, 1);
    }

    function closeMentionContainer() {
        usernameSearch = '';
        const containers = document.querySelectorAll('.mention-container');
        containers.forEach(elem => elem.remove());
    }

    function insertUsernameIntoEditor(input, username) {
        if (usernameSearch) {
            const usernameMatcher = new RegExp(`(@${usernameSearch})(?:<|\s|$)`);

            input.innerHTML = input.innerHTML
                .replace(usernameMatcher, (all, match) => {
                    const suffix = all.endsWith('<') ? ' <' : ' ';
                    return `@${username}${suffix}`;
                })
                .replace(/<p><br><\/p>$/, '');
        }

        setTimeout(() => {
            editor.setSelection(99999, 0, 'api');
            closeMentionContainer();
        }, 0);
    }

    function uploadImages(files) {
        if (files.length === 0) {
            setUploadingEnd();
            return [];
        }

        const form = new FormData();
        files.forEach(file => form.append('file', file));

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
                setUploadingEnd();
            });
    }

    function setUploadingStart() {
        selector('.uploading-images').classList.remove('d-none');

        const form = container.closest('form');

        if (form) {
            form.querySelector('button[type="submit"]').setAttribute('disabled', 'true');
        }
    }

    function setUploadingEnd() {
        selector('.uploading-images').classList.add('d-none');

        const form = container.closest('form');

        if (form) {
            form.querySelector('button[type="submit"]').removeAttribute('disabled');
        }
    }

    return editor;
}

function destroyEditor(container) {
  const selector = s => document.querySelector(`${container} ${s}`);

  const toolbar = selector('.toolbar');
  const toolbarContents = toolbar.innerHTML;
  toolbar.classList.remove('ql-toolbar');
  toolbar.innerHTML = '';
  toolbar.innerHTML = toolbarContents;

  const editor = selector('.editor');
  const editorContents = selector('.ql-editor').innerHTML;
  editor.class = 'editor';
  editor.innerHTML = '';
  editor.innerHTML = editorContents;
}

window.addEventListener('load', () => {
    document.querySelectorAll('.editor-container').forEach(container => {
        const options = container.getAttribute('data-options') || '';
        const light = container.classList.contains('light');

        const params = options.split(',').reduce((acc, key) => ({ ...acc, [key]: true }), {});
        if (light) params.light = true;

        createEditor(container, params);
    });

    document.querySelectorAll('*[data-contains-code] pre').forEach(block => {
        hljs.highlightBlock(block);
    });
});


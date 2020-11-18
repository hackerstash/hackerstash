document.addEventListener('click', (event) => {
    if (event.target.closest('.add-reply')) {
        // Delete all the other forms
        document.querySelectorAll('.comment-reply').forEach((element) => {
            element.remove();
        });

        const parent = event.target.closest('li');
        const form = document.querySelector('.comment-form').cloneNode(true);
        const input = document.createElement('input');
        const wrapper = document.createElement('div');
        const cancel = form.querySelector('.cancel');

        // Create a hidden input field with the parent comment id
        input.type = 'hidden';
        input.id = 'parent_comment_id';
        input.name = 'parent_comment_id';
        input.value = event.target.getAttribute('data-id');

        // Create the form with which to reply to the comment
        form.classList.add('reply-form');
        form.querySelector('fieldset').appendChild(input);
        form.querySelector('label').innerText = 'Reply';
        form.removeAttribute('id');

        // Create a wrapper to insert the form into
        wrapper.classList.add('comment-reply');
        wrapper.appendChild(form);

        // Remove on cancel
        cancel.addEventListener('click', (event) => {
          event.target.closest('.comment-reply').remove();
        });

        parent.parentNode.insertBefore(wrapper, parent.nextSibling);
        const container = form.querySelector('.editor-container');
        createEditor(container, { focus: true, light: true });
    }

    if (event.target.closest('.collapse') || event.target.closest('.collapse-comments')) {
        event.target.closest('li').classList.toggle('collapsed');
    }

    if (event.target.closest('.delete-comment')) {
        event.preventDefault();

        const link = event.target.closest('.delete-comment').getAttribute('href');

        const existing = document.querySelector('#delete-comment-modal');
        if (existing) existing.remove();

        const modal = document.createElement('div');
        modal.id = 'delete-comment-modal';
        modal.classList.add('modal', 'open');
        modal.innerHTML = `
            <div class="modal-body sm">
                <header>
                    <h3>Delete comment</h3>
                    <i class="icon ri-close-line modal-close"></i>
                </header>
                <main>
                    <div class="content">
                        <p>Are you sure you want to delete your comment?</p>
                    </div>
                    <footer>
                        <a class="button tertiary" href="${link}">Delete</a>
                        <button class="button secondary modal-close" type="button">Cancel</button>
                    </footer>
                </main>
            </div>
        `;
        document.body.appendChild(modal);
    }

    if (event.target.closest('.edit-comment')) {
        event.preventDefault();

        const parent = event.target.closest('li');
        const form = document.querySelector('.comment-form').cloneNode(true);
        const wrapper = document.createElement('div');
        const cancel = form.querySelector('.cancel');

        // Create the form with which to reply to the comment
        form.classList.add('reply-form');
        form.querySelector('label').innerText = 'Edit';
        form.querySelector('.ql-editor').innerHTML = parent.querySelector('.rich-text').innerHTML;
        form.querySelector('.button-group .button:first-of-type').innerText = 'Save Changes';
        form.action = event.target.getAttribute('data-url');
        form.removeAttribute('id');

        // Create a wrapper to insert the form into
        wrapper.classList.add('comment-reply');
        wrapper.appendChild(form);

        // Remove on cancel
        cancel.addEventListener('click', (event) => {
          event.target.closest('.comment-reply').remove();
          parent.classList.remove('editing');
        });

        parent.parentNode.insertBefore(wrapper, parent);
        parent.classList.add('editing');
        const container = form.querySelector('.editor-container');
        createEditor(container, { focus: true, light: true });
    }
});

document.addEventListener('submit', (event) => {
    if (event.target.classList.contains('comment-form')) {
        event.preventDefault();

        const form = new FormData(event.target);
        const link = event.target.getAttribute('action');

        const options = {
            method: 'post',
            credentials: 'include',
            headers: {
                'x-requested-with': 'fetch'
            },
            body: form
        };

        event.target.querySelector('.ql-editor').innerHTML = '';

        fetch(link, options)
            .then((response) => {
                if (response.ok) {
                    return response.text();
                }
                throw new Error(response.statusText);
            })
            .then((response) => {
                const comments = document.querySelector('.comments');
                comments.insertAdjacentHTML('afterend', response);
                comments.remove();
                const commentCount = document.querySelector('.comments').getAttribute('data-comment-count');
                document.querySelector('.comment-count').innerHTML = `${commentCount} Comments`;
            });
    }
});
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

        // Create a wrapper to insert the form into
        wrapper.classList.add('comment-reply');
        wrapper.appendChild(form);

        // Remove on cancel
        cancel.addEventListener('click', (event) => {
          event.target.closest('.comment-reply').remove();
        });

        parent.parentNode.insertBefore(wrapper, parent.nextSibling);
    }

    if (event.target.closest('.collapse') || event.target.closest('.collapse-comments')) {
        event.target.closest('li').classList.toggle('collapsed');
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

        event.target.querySelector('.textarea').value = '';

        fetch(link, options)
            .then((response) => {
                if (response.ok) {
                    return response.text();
                }
                throw new Error(response.statusText);
            })
            .then((response) => {
                document.querySelector('.comments').innerHTML = response;
            });
    }
});
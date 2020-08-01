document.addEventListener('click', function(event) {
    if (event.target.closest('.add-reply')) {
        // Delete all the other forms
        document.querySelectorAll('.comment-reply').forEach(function(element) {
            element.remove();
        });

        var parent = event.target.closest('li');
        var form = document.querySelector('.comment-form').cloneNode(true);
        var input = document.createElement('input');
        var wrapper = document.createElement('div');
        var cancel = form.querySelector('.cancel');

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
        cancel.addEventListener('click', function(event) {
          event.target.closest('.comment-reply').remove();
        });

        parent.parentNode.insertBefore(wrapper, parent.nextSibling);
    }

    if (event.target.closest('.collapse')) {
        console.log('Collapse');
    }
});

document.addEventListener('submit', function(event) {
    if (event.target.classList.contains('comment-form')) {
        event.preventDefault();

        var form = new FormData(event.target);
        var link = event.target.getAttribute('action');

        var options = {
            method: 'post',
            credentials: 'include',
            headers: {
                'x-requested-with': 'fetch'
            },
            body: form
        };

        event.target.querySelector('.textarea').value = '';

        fetch(link, options)
            .then(function(response) {
                if (response.ok) {
                    return response.text()
                }
            })
            .then(function(response) {
                document.querySelector('.comments').innerHTML = response;
            });
    }
});
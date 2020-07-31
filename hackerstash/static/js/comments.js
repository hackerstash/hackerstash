var replies = document.querySelectorAll('.add-reply');
var collapses = document.querySelectorAll('.collapse');

replies.forEach(function(reply) {
    reply.addEventListener('click', function(event) {
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
    });
});

collapses.forEach(function(collapse) {
    collapse.addEventListener('click', function(event) {
        console.log(event.target);
    });
});
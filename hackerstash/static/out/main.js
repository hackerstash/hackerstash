var file = document.getElementById('file');
var avatar = document.getElementById('avatar');
var deleteAvatarButton = document.querySelector('.delete-avatar');

if (file) {
    file.addEventListener('change', function(event) {
        var file = event.target.files[0];
        var container = document.querySelector('.edit-avatar');
        var icon = container.querySelector('.avatar');

        var img = document.createElement('img');
        img.src = URL.createObjectURL(file);

        icon.innerHTML = '';
        icon.appendChild(img);
        container.classList.remove('no-image');
    });
}

if (deleteAvatarButton) {
    deleteAvatarButton.addEventListener('click', function() {
        var container = document.querySelector('.edit-avatar');
        var icon = container.querySelector('.avatar');
        icon.innerHTML = '<span class="placeholder">$</span>';
        container.classList.add('no-image');
        file.value = '';
        avatar.value = '';
    });
}
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
var hamburger = document.querySelector('.hamburger');

var openHamburgerIcon = 'ri-menu-line';
var closeHamburgerIcon = 'ri-close-line';

if (hamburger) {
    hamburger.addEventListener('click', function(event) {
        var element = event.target;

        element.classList.toggle(openHamburgerIcon);
        element.classList.toggle(closeHamburgerIcon);

        document.getElementById('sidebar').classList.toggle('menu-open');
    });
}
var votes = document.querySelectorAll('.votes a');

votes.forEach(function(vote) {
    vote.addEventListener('click', function(event) {
//        event.preventDefault();
//
//        var link = event.target.getAttribute('href');
//
//        var options = {
//            credentials: 'include',
//            headers: {
//                'x-requested-with': 'fetch'
//            }
//        };
//
//        fetch(link, options)
//            .then(function(response) {
//                if (response.ok) {
//                    return response.text()
//                }
//            })
//            .then(function(response) {
//                console.log(response);
//            });
    });
});
var file = document.getElementById('file');
var avatar = document.getElementById('avatar');
var deleteAvatarButton = document.querySelector('.delete-avatar');

if (file) {
    file.addEventListener('change', function(event) {
        var file = event.target.files[0];
        var container = document.querySelector('.edit-avatar');

        // There are multiple image uploads, if the
        // avatar container is not available it's likely
        // something else (e.g. posts)
        if (!container) return null;

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

    if (event.target.closest('.collapse') || event.target.closest('.collapse-comments')) {
        event.target.closest('li').classList.toggle('collapsed');
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
var openModalButtons = document.querySelectorAll('.modal-open');
var closeModalButtons = document.querySelectorAll('.modal-close');

openModalButtons.forEach(function(element) {
    element.addEventListener('click', function(event) {
        var selector = event.target.closest('.modal-open').getAttribute('data-modal');
        document.querySelector('#' + selector).classList.add('open');
    });
});

closeModalButtons.forEach(function(element) {
    element.addEventListener('click', function(event) {
        event.target.closest('.modal').classList.remove('open');
    });
});

document.addEventListener('click', function(event) {
    if (event.target.closest('.modal')) {
        if (!event.target.closest('.modal-body')) {
            event.target.closest('.modal').classList.remove('open');
        }
    }
});
var file = document.getElementById('file');
var body = document.getElementById('body');

if (file) {
    file.addEventListener('change', function(event) {
        var files = event.target.files;
        var container = document.querySelector('.post-images');

        // If the container doesn't exist then it's
        // likely something else (e.g. avatars)
        if (!container) return;

        Array.from(files).forEach(function(file) {
            var img = document.createElement('img');
            var imgContainer = document.createElement('div');
            var list = document.createElement('li');
            var button = document.createElement('button');

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
            var fileNameInput = document.getElementById('filenames_to_upload');
            var fileNames = JSON.parse(fileNameInput.value);
            fileNames.push(file.name);
            fileNameInput.value = JSON.stringify(fileNames);
        });
    });
}

document.addEventListener('click', function(event) {
    if (event.target.closest('.delete-image')) {
        var filename = event.target.closest('.delete-image').getAttribute('data-file-name');

        // Delete the thumbnail
        event.target.closest('li').remove();

        var lines = body.value.split('\n');

        // Strip out any references to the file from the textarea
        body.value = lines
            .filter(function(line) {
                return !line.includes('(' + filename + ')');
            })
            .join('\n');

        // Remove the filename from the list
        var fileNameInput = document.getElementById('filenames_to_upload');
        var fileNames = JSON.parse(fileNameInput.value);
        fileNames = fileNames.filter(function(name) {
            console.log(name, filename)
            return name !== filename;
        });
        fileNameInput.value = JSON.stringify(fileNames);
    }
});
// Fetch the partials from the server so that voting
// does not cause a page refresh. If JS is disabled
// then voting will still work

document.addEventListener('click', function(event) {
    if (event.target.closest('.vote-button')) {
        event.preventDefault();

         var button = event.target.closest('.button')
         var link = button.getAttribute('href');
         var parent = button.getAttribute('data-parent');

         var options = {
             credentials: 'include',
             headers: {
                 'x-requested-with': 'fetch'
             }
        };

        fetch(link, options)
            .then(function(response) {
                if (response.ok) {
                    return response.text()
                }
            })
            .then(function(response) {
                document.querySelector('.' + parent).innerHTML = response;
            });
    }
});
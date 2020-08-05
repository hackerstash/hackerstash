var messages = document.querySelectorAll('.message');

messages.forEach(function(message) {
    var close = message.querySelector('.close-message');

    if (close) {
        close.addEventListener('click', function(event) {
            event.target.closest('.message').remove();
        });
    }
});
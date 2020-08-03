var messages = document.querySelectorAll('.message');

messages.forEach(function(message) {
    message.querySelector('.close-message').addEventListener('click', function(event) {
        event.target.closest('.message').remove();
    });
});
const messages = document.querySelectorAll('.message');

messages.forEach((message) => {
    const close = message.querySelector('.close-message');

    if (close) {
        close.addEventListener('click', (event) => {
            event.target.closest('.message').remove();
        });
    }
});
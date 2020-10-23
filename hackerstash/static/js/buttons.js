document.addEventListener('click', event => {
    if (event.target.closest('.button.disabled')) {
        event.preventDefault();
        const classList = event.target.classList;

        if (classList.contains('not-published')) {
            document.querySelector('#publish-modal').classList.add('open');
        } else if (classList.contains('logged-out')) {
            document.querySelector('#sign-up-modal').classList.add('open');
        }
    }
});
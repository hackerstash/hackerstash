const openModalButtons = document.querySelectorAll('.modal-open');

openModalButtons.forEach((element) => {
    element.addEventListener('click', (event) => {
        if (event.target.classList.contains('disabled')) return;

        event.preventDefault();
        const selector = event.target.closest('.modal-open').getAttribute('data-modal');
        document.querySelector('#' + selector).classList.add('open');
    });
});

document.addEventListener('click', (event) => {
    if (event.target.closest('.modal')) {
        if (!event.target.closest('.modal-body')) {
            event.preventDefault();
            event.target.closest('.modal').classList.remove('open');
        }
    }

    if (event.target.closest('.modal-close')) {
        event.preventDefault();
        event.target.closest('.modal').classList.remove('open');
    }
});
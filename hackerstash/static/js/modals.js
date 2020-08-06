const openModalButtons = document.querySelectorAll('.modal-open');
const closeModalButtons = document.querySelectorAll('.modal-close');

openModalButtons.forEach((element) => {
    element.addEventListener('click', (event) => {
        const selector = event.target.closest('.modal-open').getAttribute('data-modal');
        document.querySelector('#' + selector).classList.add('open');
    });
});

closeModalButtons.forEach((element) => {
    element.addEventListener('click', (event) => {
        event.target.closest('.modal').classList.remove('open');
    });
});

document.addEventListener('click', (event) => {
    if (event.target.closest('.modal')) {
        if (!event.target.closest('.modal-body')) {
            event.target.closest('.modal').classList.remove('open');
        }
    }
});
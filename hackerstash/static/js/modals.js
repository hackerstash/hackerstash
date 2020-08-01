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
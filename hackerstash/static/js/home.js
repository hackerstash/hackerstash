const accordion = document.querySelector('.accordion');

if (accordion) {
    accordion.querySelectorAll('.toggle').forEach(element => {
        element.addEventListener('click', event => {
            accordion.querySelector('.active').classList.remove('active');

            event.target.closest('li').classList.add('active');
        });
    });
}
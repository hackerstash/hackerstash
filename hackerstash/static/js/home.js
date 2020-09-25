const accordion = document.querySelector('.accordion');

if (accordion) {
    accordion.querySelectorAll('li').forEach(element => {
        element.addEventListener('click', event => {
            accordion.querySelectorAll('li').forEach(x => x.classList.remove('active'));
            document.querySelectorAll('.phone img').forEach(x => x.classList.remove('active'));

            const item = event.target.closest('li');
            item.classList.add('active');
            const tab = item.getAttribute('data-tab');
            console.log(tab);
            document.querySelector(`.phone img[data-tab="${tab}"]`).classList.add('active');
        });
    });
}
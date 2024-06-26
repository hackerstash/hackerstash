const accordion = document.querySelector('.accordion');
const carousell = document.querySelector('.phone');

if (accordion) {
    accordion.querySelectorAll('li').forEach(element => {
        element.addEventListener('click', event => {
            accordion.querySelectorAll('li').forEach(x => {
                x.classList.remove('active');
                x.setAttribute('aria-selected', 'false');
            });

            document.querySelectorAll('.phone img').forEach(x => {
                x.classList.remove('active');
                x.setAttribute('hidden', 'true');
            });

            const item = event.target.closest('li');
            item.classList.add('active');
            item.setAttribute('aria-selected', 'true');
            const tab = item.getAttribute('data-tab');
            document.querySelector(`.phone img[data-tab="${tab}"]`).classList.add('active');
            document.querySelector(`.phone img[data-tab="${tab}"]`).removeAttribute('hidden');
        });

        element.addEventListener('keyup', event => {
            if (event.keyCode == 13) {
                event.target.click();
            }
        });
    });
}

if (carousell) {
    carousell.querySelectorAll('.navigation i').forEach(element => {
        element.addEventListener('click', event => {
            const isNext = event.target.classList.contains('next');
            const total = carousell.querySelectorAll('img').length;
            const index = Number(carousell.getAttribute('data-index'));

            const newIndex = isNext ? index + 1 : index - 1;
            carousell.querySelectorAll('.navigation i').forEach(i => i.classList.remove('disabled'));
            carousell.setAttribute('data-index', newIndex);

            if (isNext && total === newIndex + 1) {
                carousell.querySelector('.navigation .next').classList.add('disabled');
            }

            if (!isNext && newIndex === 0) {
                carousell.querySelector('.navigation .prev').classList.add('disabled');
            }

            carousell.querySelectorAll('.indicators span').forEach(s => s.classList.remove('active'));
            carousell.querySelector(`.indicators span:nth-of-type(${newIndex + 1})`).classList.add('active');

            carousell.querySelectorAll('img').forEach(i => i.classList.remove('active'));
            carousell.querySelector(`img:nth-of-type(${newIndex + 1})`).classList.add('active');
        });
    });
}

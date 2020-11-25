const reviews = document.querySelector('.review-container');

document.querySelectorAll('input[type="checkbox"]').forEach(element => {
    element.addEventListener('change', event => {
        const checkbox = event.target;
        const goal = checkbox.closest('.goal');
        const body = goal.querySelector('.body');
        const arrow = goal.querySelector('.arrow');

        if (checkbox.checked) {
            body.classList.remove('d-none');
            arrow.classList.remove('toggle');
        } else {
            body.classList.add('d-none');
            arrow.classList.add('toggle');
        }
    });
});

document.querySelectorAll('.goal .arrow').forEach(element => {
    element.addEventListener('click', event => {
        event.target.closest('.goal').querySelector('input[type="checkbox"]').click();
    });
});

document.querySelectorAll('.review-container .card').forEach(element => {
   element.addEventListener('click', event => {
       const id = event.target.closest('.card').getAttribute('data-project-id');

       document.querySelectorAll('.review-container li').forEach(li => {
           li.classList.remove('active');

           if (li.querySelector('.card').getAttribute('data-project-id') === id) {
               li.classList.add('active');
           }
       });

       document.querySelectorAll('.review-body').forEach(body => {
           body.classList.add('d-none');

           if (body.getAttribute('id') === id) {
               body.classList.remove('d-none');
           }
       });
   });
});

if (reviews) {
    const selector = '.sortable-list';
    const containers = reviews.querySelectorAll(selector);

    window.addEventListener('load', () => {
        const sortable = new Sortable.default(containers, {
            draggable: '.sortable-list li',
            mirror: {
                // appendTo: selector,
                constrainDimensions: true
            }
        });

        sortable.on('drag:stop', () => {
            setTimeout(() => {
                reviews.querySelectorAll('.position').forEach((element, index) => {
                    element.innerHTML = `<span>${index + 1}</span>`;
                });

                const order = Array.from(reviews.querySelectorAll('li')).map(element => element.getAttribute('data-project-id'));

                document.querySelectorAll('.review-body').forEach(element => {
                   const id = element.getAttribute('id');
                   const input = element.querySelector('input[type="hidden"]');
                   input.value = order.findIndex(o => o === id);
                });
            }, 0);
        });
    });
}
document.querySelectorAll('input[type="checkbox"]').forEach(element => {
    element.addEventListener('change', event => {
        const checkbox = event.target;
        const goal = checkbox.closest('.goal');
        const body = goal.querySelector('.body');

        if (checkbox.checked) {
            body.classList.remove('d-none');
        } else {
            body.classList.add('d-none');
        }
    });
});
const waitlistFilter = document.querySelector('.waitlist-filter');

if (waitlistFilter) {
    waitlistFilter.addEventListener('keyup', (event) => {
        document.querySelectorAll('.waitlist-list li').forEach(element => {
            element.classList.remove('d-none');

            if (!element.innerText.includes(event.target.value)) {
                element.classList.add('d-none');
            }
        });
    });
}
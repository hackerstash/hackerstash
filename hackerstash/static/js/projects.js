const projectSorting = document.querySelector('#sorting');
const description = document.querySelector('#description');

if (projectSorting) {
    projectSorting.addEventListener('change', (event) => {
        const searchParams = new URLSearchParams(window.location.search);
        searchParams.set('sorting', event.target.value);
        window.location.search = searchParams.toString();
    });
}

if (description) {
    description.addEventListener('keyup', (event) => {
        event.target.classList.remove('error');

        if (event.target.value.length > 280) {
            event.preventDefault();
            event.target.classList.add('error');
        }
    });
}

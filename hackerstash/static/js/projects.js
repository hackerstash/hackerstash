const projectSorting = document.querySelector('#sorting');

if (projectSorting) {
    projectSorting.addEventListener('change', (event) => {
        const searchParams = new URLSearchParams(window.location.search);
        searchParams.set('sorting', event.target.value);
        window.location.search = searchParams.toString();
    });
}
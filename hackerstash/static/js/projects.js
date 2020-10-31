const projectSorting = document.querySelector('#sorting');
const description = document.querySelector('#description');
const headerFile = document.querySelector('#header_file');
const projectShow = document.querySelector('#project-show');

if (projectSorting) {
    projectSorting.addEventListener('change', event => {
        const searchParams = new URLSearchParams(window.location.search);
        searchParams.set('sorting', event.target.value);
        window.location.search = searchParams.toString();
    });
}

if (description) {
    description.addEventListener('keyup', event => {
        event.target.classList.remove('error');

        if (event.target.value.length > 280) {
            event.preventDefault();
            event.target.classList.add('error');
        }
    });
}

if (headerFile) {
    headerFile.addEventListener('change', event => {
        event.target.closest('form').submit();
    });
}

if (projectShow) {
    projectShow.querySelectorAll('input').forEach(element => {
        element.addEventListener('change', event => {
            // TODO fetch a partial
            event.target.closest('form').submit();
        });
    });
}
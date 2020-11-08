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
        const header = document.querySelector('.project-header');
        const label = header.querySelector('label');
        header.classList.add('loading');
        label.querySelector('i').remove();
        const spinner = document.createElement('div');
        spinner.classList.add('spinner', 'md');
        label.appendChild(spinner);
        event.target.closest('form').submit();
    });
}

if (projectShow) {
    projectShow.querySelectorAll('input').forEach(element => {
        element.addEventListener('change', event => {
            const form = event.target.closest('form');
            const formData = new FormData(form);
            const query = new URLSearchParams(formData).toString();
            const link = `${form.getAttribute('action')}?${query}`;
            fetchProjectFeed(link);

            if (document.querySelectorAll('.checkbox-group input[type="checkbox"]:checked').length === 0) {
                document.querySelectorAll('.checkbox-group input[type="checkbox"]').forEach(c => {
                    c.checked = true;
                });
            }
        });
    });
}

document.addEventListener('click', event => {
    if (event.target.id == 'load-more-feed') {
        event.preventDefault();

        const link = event.target.getAttribute('href');
        fetchProjectFeed(link);
    }
});

function fetchProjectFeed(link) {
    const options = {
        method: 'get',
        credentials: 'include',
        headers: {
            'x-requested-with': 'fetch'
        }
    };

    fetch(link, options)
        .then((response) => {
            if (response.ok) {
                return response.text();
            }
            throw new Error(response.statusText);
        })
        .then((response) => {
            const feed = document.querySelector('.feed');
            feed.insertAdjacentHTML('afterend', response);
            feed.remove();
        });
}
// Fetch the partials from the server so that voting
// does not cause a page refresh. If JS is disabled
// then voting will still work

document.addEventListener('click', (event) => {
    if (event.target.closest('.vote-button')) {
        event.preventDefault();

         const button = event.target.closest('.button')
         const link = button.getAttribute('href');
         const parent = button.getAttribute('data-parent');

         const options = {
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
                document.querySelector('.' + parent).innerHTML = response;
            });
    }
});
// Fetch the partials from the server so that voting
// does not cause a page refresh. If JS is disabled
// then voting will still work

document.addEventListener('click', (event) => {
    if (event.target.closest('.vote-button')) {
        event.preventDefault();

        const button = event.target.closest('.button')
        const link = button.getAttribute('href');
        const parent = button.getAttribute('data-parent');

        if (button.closest('.disabled')) {
            const message = getDisabledToastMessage(button.closest('.disabled').classList);
            return createToast(message);
        }

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

    function getDisabledToastMessage(classList) {
        if (classList.contains('logged-out')) {
            return 'You can\'t vote because you’re currently logged out.';
        }

        if (classList.contains('not-published')) {
            return 'You can\'t vote because you do not have a published project.';
        }

        if (classList.contains('own-project')) {
            return 'You can\'t vote on your own project.';
        }

        return 'An unknown error has occurred, please try again.'
    }
});
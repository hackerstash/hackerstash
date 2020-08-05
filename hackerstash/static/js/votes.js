// Fetch the partials from the server so that voting
// does not cause a page refresh. If JS is disabled
// then voting will still work

document.addEventListener('click', function(event) {
    if (event.target.closest('.vote-button')) {
        event.preventDefault();

         var button = event.target.closest('.button')
         var link = button.getAttribute('href');
         var parent = button.getAttribute('data-parent');

         var options = {
             credentials: 'include',
             headers: {
                 'x-requested-with': 'fetch'
             }
        };

        fetch(link, options)
            .then(function(response) {
                if (response.ok) {
                    return response.text()
                }
            })
            .then(function(response) {
                console.log(parent);
                document.querySelector('.' + parent).innerHTML = response;
            });
    }
});
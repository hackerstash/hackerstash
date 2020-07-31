var votes = document.querySelectorAll('.votes a');

votes.forEach(function(vote) {
    vote.addEventListener('click', function(event) {
//        event.preventDefault();
//
//        var link = event.target.getAttribute('href');
//
//        var options = {
//            credentials: 'include',
//            headers: {
//                'x-requested-with': 'fetch'
//            }
//        };
//
//        fetch(link, options)
//            .then(function(response) {
//                if (response.ok) {
//                    return response.text()
//                }
//            })
//            .then(function(response) {
//                console.log(response);
//            });
    });
});
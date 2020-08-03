var locationTypeahead = document.querySelector('.location-typeahead');
var locationOutput = document.querySelector('.search-results');

if (locationTypeahead) {
    locationTypeahead.addEventListener('keyup', function(event) {
        locationOutput.innerHTML = '';

        if (event.target.value === '') return;

        fetch('/api/locations?q=' + event.target.value)
            .then(function(response) {
                return response.json();
            })
            .then(function(locations) {
                var results = document.createElement('div');
                results.classList.add('results');

                locations.forEach(function(location) {
                    var button = document.createElement('button');
                    button.type = 'button';
                    button.classList.add('button');
                    button.onclick = function() {
                        locationTypeahead.value = location;
                        locationOutput.innerHTML = '';
                    }
                    button.innerText = location;
                    results.appendChild(button);
                });

                locationOutput.appendChild(results);
            });
    });
}
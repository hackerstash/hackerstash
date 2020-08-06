const locationTypeahead = document.querySelector('.location-typeahead');
const locationOutput = document.querySelector('.search-results');

if (locationTypeahead) {
    locationTypeahead.addEventListener('keyup', (event) => {
        locationOutput.innerHTML = '';

        if (event.target.value === '') return;

        fetch('/api/locations?q=' + event.target.value)
            .then((response) =>response.json())
            .then((locations) => {
                const results = document.createElement('div');
                results.classList.add('results');

                locations.forEach((location) => {
                    const button = document.createElement('button');
                    button.type = 'button';
                    button.classList.add('button');
                    button.onclick = () => {
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
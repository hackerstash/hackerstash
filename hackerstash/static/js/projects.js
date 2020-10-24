const projectSorting = document.querySelector('#sorting');
const projectChart = document.querySelector('#project-graph');
const description = document.querySelector('#description');

if (projectSorting) {
    projectSorting.addEventListener('change', (event) => {
        const searchParams = new URLSearchParams(window.location.search);
        searchParams.set('sorting', event.target.value);
        window.location.search = searchParams.toString();
    });
}

if (projectChart) {
    const myBarChart = new Chart(projectChart, {
        type: 'bar',
        options: {
            tooltips: {
                enabled: false
            },
            legend: {
                display: false
            },
            scales: {
                yAxes: [
                    {
                        ticks: {
                            fontColor: '#DEE7FF',
                            beginAtZero: true,
                            callback: val => val % 1 === 0 ? val : undefined,
                        },
                        gridLines: {
                            color: '#101F3E',
                            drawBorder: false
                        }
                    }
                ],
                xAxes: [
                    {
                        ticks: {
                            fontColor: '#DEE7FF',
                            autoSkip: false
                        },
                        gridLines: {
                            display: false
                        }
                    }
                ]
            }
        },
        data: {
            labels: daysLabelsForThisMonth(),
            datasets: [
                {
                    label: '# of points',
                    data: JSON.parse(window.projectScoreData),
                    backgroundColor: '#3EF57D',
                    barThickness: 25
                }
            ]
        }
    });

    function daysLabelsForThisMonth() {
        const count = new Date(2020, 10, 0).getDate();
        return [...Array(count).keys()].map(x => '' + (x + 1));
    }
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

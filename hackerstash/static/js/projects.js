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
    var myBarChart = new Chart(projectChart, {
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
                            callback: val => val % 1 === 0 ? val : undefined
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
                            fontColor: '#DEE7FF'
                        },
                        gridLines: {
                            display: false
                        }
                    }
                ]
            }
        },
        data: {
            labels: ['1', '2', '3', '4', '5', '6', '7'],
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

document.querySelectorAll('.edit-task-modal .edit-task').forEach(element => {
    element.addEventListener('click', (event) => {
        const modal = event.target.closest('.edit-task-modal');
        modal.querySelector('.show-view').classList.add('d-none');
        modal.querySelector('.edit-view').classList.remove('d-none');
        modal.querySelector('header h3').innerText = 'Edit Task';
        event.target.classList.add('d-none');
        createEditor('#' + modal.id);
    });
});

document.querySelectorAll('.edit-task-modal .show-task').forEach(element => {
    element.addEventListener('click', (event) => {
        const modal = event.target.closest('.edit-task-modal');
        modal.querySelector('.show-view').classList.remove('d-none');
        modal.querySelector('.edit-view').classList.add('d-none');
        modal.querySelector('header h3').innerText = 'Task';
        modal.querySelector('.edit-task').classList.remove('d-none');
        destroyEditor('#' + modal.id);
    });
});
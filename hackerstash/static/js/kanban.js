const hasKanban = document.querySelector('.has-kanban');
const hasKanbanSettings = document.querySelector('#kanban-settings');

if (hasKanban) {
    const containers = document.querySelectorAll('.columns .cards');

    const sortable = new Sortable.default(containers, {
        draggable: '.cards .card',
        mirror: {
            constrainDimensions: true,
        }
    });

    sortable.on('drag:start', (event) => {
        const disabled = event.data.originalSource.classList.contains('disabled');
        if (disabled) {
            event.cancel();
        }
    });

     sortable.on('drag:stop', (event) => {
        setTimeout(() => {
            const element = event.data.originalSource;
            const column = element.closest('.column').getAttribute('data-column');
            const projectId = element.getAttribute('data-project-id');
            const progressId = element.getAttribute('data-progress-id');
            const link = `/projects/${projectId}/progress/${progressId}`;

            const form = new FormData();
            form.append('column', column);

            const options = {
                method: 'post',
                credentials: 'include',
                headers: {
                    'x-requested-with': 'fetch'
                },
                body: form
            };

            fetch(link, options);
        }, 1);
     });
}

if (hasKanbanSettings) {
    const addColumn = document.querySelector('.add-column');
    const containers = document.querySelectorAll('#kanban-settings .columns');

    new Sortable.default(containers, {
        draggable: '#kanban-settings li',
        mirror: {
            constrainDimensions: true,
        }
    });

    if (addColumn) {
        addColumn.addEventListener('click', (event) => {
            const row = `
              <li>
                <i class="ri-drag-move-2-fill drag"></i>
                <input name="column" class="input mb-0" type="text" required>
                <i class="ri-close-line remove"></i>
              </li>
            `;

            hasKanbanSettings.querySelector('.columns').innerHTML += row;
        });
    }
}
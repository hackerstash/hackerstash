const hasKanban = document.querySelector('.has-kanban');

if (hasKanban) {
    const containers = document.querySelectorAll('.stacked-list');

    const sortable = new Sortable.default(containers, {
        draggable: '.draggable',
        mirror: {
            constrainDimensions: true,
        }
    });
}
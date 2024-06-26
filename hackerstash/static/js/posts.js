document.addEventListener('click', event => {
    if (event.target.closest('.add-choice-button')) {
        const lastPollRow = document.querySelector('.poll-row:last-of-type');
        const newPollRow = lastPollRow.cloneNode(true);

        const choice = Number(lastPollRow.getAttribute('data-choice')) + 1;
        const input = newPollRow.querySelector('input');

        setPollPosition(newPollRow, choice);
        lastPollRow.parentNode.insertBefore(newPollRow, lastPollRow.nextSibling);
    }

    if (event.target.closest('.delete-choice')) {
        event.target.closest('.poll-row').remove();

        document.querySelectorAll('.poll-row').forEach((element, index) => {
            setPollPosition(element, index + 1);
        });
    }

    if (event.target.closest('.view-results')) {
        event.target.closest('.post-poll').classList.toggle('answered');
    }

    if (event.target.closest('.hide-results')) {
        event.target.closest('.post-poll').classList.toggle('answered');
    }

    if (event.target.closest('.submit-poll')) {
        const classList = event.target.closest('.submit-poll').classList;

        if (classList.contains('disabled')) {
            event.preventDefault();

            if (classList.contains('not-published')) {
                return document.querySelector('#publish-modal').classList.add('open');
            } else if (classList.contains('logged-out')) {
                return document.querySelector('#sign-up-modal').classList.add('open');
            }
        }
    }

    function setPollPosition(element, number) {
        const input = element.querySelector('input');
        element.setAttribute('data-choice', number);
        input.id = `choice_${number}`;
        input.name = `choice_${number}`;
        input.value = '';
        input.placeholder = `Choice ${number}`;
    }
});
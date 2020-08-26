function itsPartyTime() {
    const canvas = document.createElement('canvas');
    canvas.id = 'confetti';
    canvas.style = 'left: 0; position: absolute; top: 0;';
    document.body.appendChild(canvas);

    const confettiSettings = {
        max: 1000,
        target: 'confetti'
    };

    window.confetti = new ConfettiGenerator(confettiSettings);
    confetti.render();

    const options = {
        credentials: 'include',
        headers: {
            'x-requested-with': 'fetch'
        }
    };

    fetch('/challenges/dismiss', options);
}

function partysOver() {
    window.confetti.clear();
    document.querySelector('#confetti').remove();
    document.querySelector('.challenge-completed').remove();
}
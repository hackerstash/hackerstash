function itsPartyTime() {
    const canvas = document.createElement('canvas');
    canvas.id = 'confetti';
    canvas.style = 'left: 0; position: absolute; top: 0;';
    document.body.appendChild(canvas);

    const confettiSettings = {
        max: 1000,
        size: 2,
        props: ['square'],
        target: 'confetti',
        colors: [[36, 114, 211], [112, 176, 255], [62, 245, 125], [225, 227, 62], [255, 60, 95], [176, 188, 220], [245, 150, 62]],
        clock: 75,
        respawn: false
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
document.addEventListener('click', event => {
    const badge = event.target.closest('.winner-badge');

    if (badge) {
        const stats = JSON.parse(badge.getAttribute('data-stats'));

        const first = stats[1] || 0;
        const second = stats[2] || 0;
        const third = stats[3] || 0;

        if (badge.classList.contains('detailed')) {
            badge.classList.remove('detailed');
            badge.innerHTML = `<i class="ri-trophy-line"></i> x ${first + second + third}`;
        } else {
            badge.classList.add('detailed');
            badge.innerHTML = `<span>🥇 x ${first}</span> <span>🥈 x ${second}</span> <span>🥉 x ${third}</span>`;
        }
    }
});
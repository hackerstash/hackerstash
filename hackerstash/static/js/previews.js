const previews = document.querySelectorAll('.preview');

function removePreviewCard() {
    if (window.card) {
        document.body.removeChild(window.card);
        delete window.card;
    }
}

previews.forEach((preview) => {
    preview.addEventListener('mouseenter', (event) => {
        removePreviewCard()

        const element = event.target.closest('.preview')
        const data = JSON.parse(element.getAttribute('data-preview'));
        const coords = element.getBoundingClientRect();
        const card = document.createElement('div');

        card.classList.add('preview-card');

        const lists = data.lists.map(l => `
            <li>
                <p class="small">${l.key}</p>
                <p class="small truncate">${l.value}</p>
            </li>
        `).join('');

        card.innerHTML = `
            <div class="card-header">
                <span class="avatar">
                    <img src="https://images.hackerstash.com/${data.avatar}">
                </span>
                <h4>${data.name}</h4>
            </div>
            <p class="small">${data.description}</p>
            <ul class="display-options">
                ${lists}
            </ul>
        `;
        card.style.left = coords.left + 'px';
        card.style.top = (coords.top + 40) + 'px';

        card.addEventListener('mouseleave', (event) => {
            removePreviewCard();
        });

        document.body.appendChild(card);
        window.card = card;
    });

    preview.addEventListener('mouseleave', (event) => {
        if (window.cardtimeout) {
            clearTimeout(window.cardtimeout);
            delete window.cardtimeout;
        }

        window.cardtimeout = setTimeout(() => {
            const hoveredElements = Array.from(document.querySelectorAll(':hover'));

            // Mouse has moved off screen
            if (hoveredElements.length === 0) {
                return removePreviewCard();
            }

            const isHoveredOverCard = !!hoveredElements.pop().closest('.preview-card');
            if (!isHoveredOverCard) removePreviewCard();
        }, 500);
    });
});
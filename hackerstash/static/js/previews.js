const previews = document.querySelectorAll('.preview');

previews.forEach((preview) => {
    preview.addEventListener('mouseenter', (event) => {
        const element = event.target.closest('.preview')
        const data = JSON.parse(element.getAttribute('data-preview'));
        const coords = element.getBoundingClientRect();
        const card = document.createElement('div');

        card.classList.add('preview-card');
        card.innerHTML = `
            <div class="card-header">
                <span class="avatar">
                    <img src="https://images.hackerstash.com/${data.avatar}">
                </span>
                <h4>${data.name}</h4>
            </div>
            <p class="small">${data.description}</p>
            <ul class="display-options">
                ${data.lists.map(l => `
                    <li>
                        <p class="small">${l.key}</p>
                        <p class="small truncate">${l.value}</p>
                    </li>
                `).join('')}
            </ul>
        `;
        card.style.left = coords.left + 'px';
        card.style.top = (coords.top + 40) + 'px';

        document.body.appendChild(card);
        window.card = card;
    });

    preview.addEventListener('mouseleave', (event) => {
        if (window.card) document.body.removeChild(window.card);
    });
});
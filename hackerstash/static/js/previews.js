const projectPreviews = document.querySelectorAll('.project-preview');

projectPreviews.forEach((preview) => {
    preview.addEventListener('mouseenter', (event) => {
        const element = event.target.closest('.project-preview')
        const data = JSON.parse(element.getAttribute('data-project'));
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
                <li>
                    <p class="small">Tournament position</p>
                    <p class="small">${data.position}</p>
                </li>
                <li>
                    <p class="small">Points</p>
                    <p class="small">${data.vote_score}</p>
                </li>
                <li>
                    <p class="small">Team members</p>
                    <p class="small">${data.team_members}</p>
                </li>
                <li>
                    <p class="small">Website (URL)</p>
                    <p class="small truncate">${data.url}</p>
                </li>
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
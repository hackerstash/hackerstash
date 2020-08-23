function createToast(message, type = '') {
    const toast = document.createElement('div');
    toast.classList.add('toast', type);
    toast.innerHTML = `
       <i class="ri-error-warning-line"></i>
       <p>${message}</p>
    `;

    document.querySelectorAll('.toast').forEach(element => element.remove());
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
}

if (/saved=1/.test(location.search)) {
    createToast('Changes saved', 'success')
}
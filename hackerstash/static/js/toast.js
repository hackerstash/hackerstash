function createToast(message) {
    const toast = document.createElement('div');
    toast.classList.add('toast');
    toast.innerHTML = `
       <i class="ri-error-warning-line"></i>
       <p>${message}</p>
    `;

    document.querySelectorAll('.toast').forEach(element => element.remove());
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
}
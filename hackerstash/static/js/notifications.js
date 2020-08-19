const bell = document.querySelector('.notification-bell');

if (bell) {
    window.addEventListener('blur', () => {
        stopPolling();
    });

    window.addEventListener('focus', () => {
        pollForNotifications();
    });

    function stopPolling() {
        clearTimeout(window.notificationPolling);
    }

    function pollForNotifications() {
        stopPolling();

        window.notificationPolling = setTimeout(() => {
            const options = {
                credentials: 'include',
                headers: {
                    'x-requested-with': 'fetch'
                }
            };

            fetch('/notifications/count', options)
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    }
                    throw new Error(response.statusText);
                })
                .then((response) => {
                    bell.setAttribute('data-count', response.count);

                    if (response.count > 0) {
                        bell.classList.add('unread');
                    } else {
                        bell.classList.remove('unread');
                    }

                    pollForNotifications();
                });
        }, 5000);
    }

    pollForNotifications();
}
var checkoutButton = document.getElementById('checkout-button');

if (checkoutButton) {
    checkoutButton.addEventListener('click', async () => {
        try {
            const customer = await createCustomer();
            const { session } = await createSession(customer.customer_id);

            console.log(session);

            const result = stripe.redirectToCheckout({ sessionId: session.id });
            console.log(result);
        } catch(error) {
            console.error(error);
            alert('Error');
        }
    });
}

async function createCustomer() {
    const response = await fetch('/stripe/customer', {
        method: 'post',
        credentials: 'include',
        headers: {
            'x-requested-with': 'fetch'
        }
    });
    if (response.ok) {
        return response.json();
    }
    throw new Error(response.statusText);
}

async function createSession(customerId) {
    const response = await fetch('/stripe/session', {
        method: 'post',
        credentials: 'include',
        headers: {
            'x-requested-with': 'fetch'
        }
    });
    if (response.ok) {
        return response.json();
    }
    throw new Error(response.statusText);
}
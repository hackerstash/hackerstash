const prizes = document.querySelector('#prizes');

if (prizes) {
    document.querySelector('#top_up').addEventListener('keyup', (event) => {
        const value = event.target.value;
        const contribution = document.querySelector('.subscription-contribution').getAttribute('data-value');
        const total = Number(value) + Number(contribution);

        const element = document.querySelector('.total-prize-pool');
        element.innerText = `$${total}`;
        element.setAttribute('data-value', total);
        calculateTotal();
    });

    document.querySelectorAll('.prize-value input').forEach(element => {
        element.addEventListener('keyup', (event) => {
            calculateTotal();
        });
    });

    function calculateTotal() {
        let total = 0;
        const prizePool = document.querySelector('.total-prize-pool').getAttribute('data-value');

        document.querySelectorAll('.prize-value input').forEach(element => {
            total += Number(element.value);
        });

        const element =  document.querySelector('#prize-total');

        element.value = total;
        element.classList.remove('error');
        if (total > Number(prizePool)) element.classList.add('error');
    }

    calculateTotal();
}
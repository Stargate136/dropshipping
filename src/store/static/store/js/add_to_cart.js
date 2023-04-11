export function addEventsListenersQuantity(incrementButton, decrementButton, quantityInput) {

    // Ajout de gestionnaires d'événements aux boutons
    incrementButton.addEventListener("click", function(event) {
        event.preventDefault();
        // Conversion de la valeur en nombre et ajout de 1
        let currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
    });

    decrementButton.addEventListener("click", function(event) {
        event.preventDefault();
        // Conversion de la valeur en nombre et soustraction de 1
        let currentValue = parseInt(quantityInput.value);
        // Vérification que la valeur est supérieure à 1 pour éviter d'avoir des nombres négatifs
        if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
        }
    });
}

export function addEventListenerAddToCart(addToCartLink, quantityInput, redirect) {
    // Ajout de gestionnaires d'événements aux boutons
    addToCartLink.addEventListener("click", function(event) {
        event.preventDefault();
        const quantityValue = parseInt(quantityInput.value);
        addToCartLink.href += `?quantity=${quantityValue}`;
        addToCartLink.href += `&redirect=${redirect}`;
        window.location.href = addToCartLink.href;
    })
}


function addEventsListenersQuantity() {
    // Récupération des éléments HTML nécessaires
    const incrementButton = document.getElementById("increment");
    const decrementButton = document.getElementById("decrement");
    const quantityInput = document.getElementById("quantity");

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

function addEventListenerAddToCart() {
    // Récupération des éléments HTML nécessaire
    const quantityInput = document.getElementById("quantity");
    const addToCartLink = document.getElementById("add-to-cart");

    // Ajout de gestionnaires d'événements aux boutons
    addToCartLink.addEventListener("click", function(event) {
        event.preventDefault();
        const quantityValue = parseInt(quantityInput.value);
        addToCartLink.href += `?quantity=${quantityValue}`;
        window.location.href = addToCartLink.href;
    })
}

addEventsListenersQuantity()
addEventListenerAddToCart()
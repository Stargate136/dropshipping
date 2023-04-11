import { addEventsListenersQuantity } from "./add_to_cart.js";

const quantities = document.querySelectorAll(".quantity");

for (let quantityDiv of quantities) {
    // Récupération des éléments HTML nécessaires
    const incrementButton = quantityDiv.querySelector("[data-role=increment]");
    const decrementButton = quantityDiv.querySelector("[data-role=decrement]");
    const quantityInput = quantityDiv.querySelector("[data-role=value]");

    // Ajout des listeners
    addEventsListenersQuantity(incrementButton, decrementButton, quantityInput);
};

const deleteLinks = document.querySelectorAll(".delete-button");

for (let deleteLink of deleteLinks) {
    deleteLink.addEventListener("click", function(event) {
        event.preventDefault();
        const slug = deleteLink.dataset.slug;
        const href = `delete-order/${slug}`
        window.console.log(href)
        window.location.href = href;
        
    });
};

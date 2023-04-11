import { addEventsListenersQuantity, addEventListenerAddToCart } from "./add_to_cart.js";

// Récupération des éléments HTML nécessaires
const incrementButton = document.getElementById("increment");
const decrementButton = document.getElementById("decrement");
const quantityInput = document.getElementById("quantity");
const addToCartLink = document.getElementById("add-to-cart");



addEventsListenersQuantity(incrementButton, decrementButton, quantityInput)
addEventListenerAddToCart()
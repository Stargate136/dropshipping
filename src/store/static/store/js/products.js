import { addEventsListenersQuantity, addEventListenerAddToCart } from "./add_to_cart.js";

// CATEGORIES
const buttonsCategory = document.querySelectorAll(".category-link");

for (let button of buttonsCategory ) {
    button.addEventListener("click", function(event) {
        
        event.preventDefault();

        const categories = document.querySelectorAll(".show-grid");
        for (let category of categories ) {
            category.classList.remove("show-grid");
            category.classList.add("hide-grid");
        }

        const id = button.dataset.id;
        const productsCategory = document.querySelector(`.products-category[data-id=${id}`);
        productsCategory.classList.add("show-grid");
    });
};

// ADD TO CART

const products = document.querySelectorAll(".add-to-cart");

window.console.log(products);

for (let product of products) {

    // Récupération des éléments HTML nécessaires
    const incrementButton = product.querySelector("[data-role=increment]");
    const decrementButton = product.querySelector("[data-role=decrement]");
    const quantityInput = product.querySelector("[data-role=quantity]");
    const addToCartLink = product.querySelector("[data-role=add-to-cart]");

    const redirect = "store:products-list"

    addEventsListenersQuantity(incrementButton, decrementButton, quantityInput);
    addEventListenerAddToCart(addToCartLink, quantityInput, redirect);
};
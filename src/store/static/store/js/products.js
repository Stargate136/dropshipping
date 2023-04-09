const buttonsCategory = document.querySelectorAll(".category-link");


for (let button of buttonsCategory ) {
    button.addEventListener("click", function(event) {
        
        event.preventDefault();

        categories = document.querySelectorAll(".show-grid");
        for (let category of categories ) {
            category.classList.remove("show-grid");
            category.classList.add("hide-grid");
        }

        const id = button.dataset.id;
        const productsCategory = document.querySelector(`.products-category[data-id=${id}`);
        productsCategory.classList.add("show-grid");
    });
}
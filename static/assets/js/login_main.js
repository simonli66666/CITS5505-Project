//click Share A Recipe open the recipe input box

const recipe_box = document.querySelector(".recipe_box");
const recipeOpen = document.querySelector("#openShi");
const recipeClose = recipe_box.querySelector(".close_svg svg");
recipeOpen.addEventListener("click", () => {
  recipe_box.classList.add("show");
});
recipeClose.addEventListener("click", () => {
  recipe_box.classList.remove("show");
});

document.querySelector('.recipe-search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.querySelector('.recipe-search-input').value;
    window.location.href = `/recipes?search_query=${query}`;
});


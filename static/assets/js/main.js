(() => {
  const sihpush = document.querySelector(".recipe_box");
  const openShi = document.querySelector("#openShi");
  const shipuColse = sihpush.querySelector(".close_svg svg");
  openShi.addEventListener("click", () => {
    sihpush.classList.add("show");
  });
  shipuColse.addEventListener("click", () => {
    sihpush.classList.remove("show");
  });
})();

const login_box = document.querySelector("#login");

const close = login_box.querySelector(".close");

const con = document.querySelector(".con");

const show_logins = document.querySelectorAll(".show_login");

close.onclick = function () {
  // login_box.style.display = 'none';
  login_box.classList.add("show");
};

// con.onclick = function (e) {
//   e.stopPropagation();
// }

close.onclick = function () {
  // login_box.style.display = 'none';
  login_box.classList.remove("show");
};

// window.onclick = function (e) {
//   if (e.target == login_box) {
//     login_box.style.display = 'none';
//   }
// }

for (let show_login of show_logins) {
  show_login.addEventListener("click", function () {
    //   login_box.style.display = 'block';
    login_box.classList.add("show");
  });
}

// document.querySelector('.register').onclick = function () {
//   login_box.style.display = 'block';
// }

const register = document.querySelector("#register");

const close2 = register.querySelector(".close");

const con2 = document.querySelector(".con");

close2.onclick = function () {
  // register.style.display = 'none';
  register.classList.add("show");
};

con2.onclick = function (e) {
  e.stopPropagation();
};

close2.onclick = function () {
  // register.style.display = 'none';
  register.classList.remove("show");
};
document.querySelector("#show_register").onclick = function () {
  //   login_box.style.display = 'block';
  register.classList.add("show");
};
document.querySelector("#show_register2").onclick = function () {
  //   register.style.display = 'block';
  register.classList.add("show");
};

//click Share A Recipe open the recipe input box

// const recipe_box = document.querySelector(".recipe_box");
// const recipeOpen = document.querySelector("#openShi");
// const recipeClose = recipe_box.querySelector(".close_svg svg");
// recipeOpen.addEventListener("click", () => {
//   recipe_box.classList.add("show");
// });
// recipeClose.addEventListener("click", () => {
//   recipe_box.classList.remove("show");
// });

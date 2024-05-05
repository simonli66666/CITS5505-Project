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

//Login form verification error message pops up
/* let ERROR = ``;
const loginBt = document.querySelector("#login .btn_x");
const registerBt = document.querySelector("#register .btn_x");

loginBt.addEventListener("click", (event) => {
  event.preventDefault();

  const inputAll = document.querySelectorAll("#login input");
  const name = inputAll[0].value;
  const password = inputAll[1].value;
  if (!password || !name) {
    document.querySelector("#login .message_box").classList.add("show");
    // document.querySelector('#login .message_box').innerHTML = `sb`
    return;
  }
  console.log(document.querySelector("#show_login"));
  document.querySelector("#login").classList.remove("show");
  document.querySelector("#show_login").style.display = "none";
  document.querySelector("#show_register").style.display = "none";
  document.querySelector(".right-header .user_pirc").style.display = "flex";
});

registerBt.addEventListener("click", (event) => {
  event.preventDefault();

  const inputAll = document.querySelectorAll("#register input");
  const name = inputAll[0].value;
  const password = inputAll[1].value;
  if (!password || !name) {
    document.querySelector("#register .message_box").classList.add("show");
    // document.querySelector('#register .message_box').innerHTML = `sb`
  }
});
 */

let ERROR = ``;
const loginBt = document.querySelector("#login .btn_x");
const registerBt = document.querySelector("#register .btn_x");

loginBt.addEventListener("click", (event) => {
  // 移除 preventDefault，允许表单提交，只在验证失败时调用
  const inputAll = document.querySelectorAll("#login input");
  const name = inputAll[0].value;
  const password = inputAll[1].value;
  if (!password || !name) {
    event.preventDefault(); // 阻止表单提交
    document.querySelector("#login .message_box").classList.add("show");
    return;
  }
  // 如果验证通过，不需要阻止表单提交，因此不调用 event.preventDefault();
  document.querySelector("#login").classList.remove("show");
  document.querySelector("#show_login").style.display = "none";
  document.querySelector("#show_register").style.display = "none";
  document.querySelector(".right-header .user_pirc").style.display = "flex";
});

registerBt.addEventListener("click", (event) => {
  // 移除 preventDefault，允许表单提交，只在验证失败时调用
  const inputAll = document.querySelectorAll("#register input");
  const name = inputAll[0].value;
  const password = inputAll[1].value;
  if (!password || !name) {
    event.preventDefault(); // 阻止表单提交
    document.querySelector("#register .message_box").classList.add("show");
  }
  // 如果验证通过，不需要阻止表单提交，因此不调用 event.preventDefault();
});

window.onload = function() {
  setTimeout(function() {
    const messages = document.querySelectorAll('.flash-message');
    messages.forEach(function(message) {
      message.style.opacity = '0';
      setTimeout(function() {
        message.style.display = 'none';
      }, 600); // 额外的延迟以允许淡出效果
    });
  }, 4000); // 4000 毫秒 = 4 秒
};

/* window.onload = function() {
  var errorPresent = {{ error|tojson }};
  if (errorPresent) {
      document.getElementById('registerModal').style.display = 'block';
  }
}; */
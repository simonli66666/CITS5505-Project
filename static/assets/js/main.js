document.addEventListener("DOMContentLoaded", function() {
    const loginBox = document.querySelector("#login");
    const registerBox = document.querySelector("#register");
    const loginClose = loginBox.querySelector(".close");
    const registerClose = registerBox.querySelector(".close");
    const havingAccount = document.querySelector(".havingAccount");
    const showRegister2 = document.querySelector("#show_register2");
  
    document.querySelectorAll("#show_login").forEach(btn => {
        btn.addEventListener("click", () => {
            loginBox.classList.add("show");
        });
    });
  
    document.querySelectorAll(".show_login").forEach(btn => {
        btn.addEventListener("click", () => {
            loginBox.classList.add("show");
        });
    });

    document.querySelector("#show_register").addEventListener("click", () => {
        registerBox.classList.add("show");
    });

    if(showRegister2) {
        showRegister2.addEventListener("click", () => {
            registerBox.classList.add("show");
        });
    }

    loginClose.addEventListener("click", () => {
        loginBox.classList.remove("show");
    });
  
    registerClose.addEventListener("click", () => {
        registerBox.classList.remove("show");
    });


    havingAccount.addEventListener("click", () => {
        registerBox.classList.remove("show");
        loginBox.classList.add("show");
    })
  
    // 登录和注册窗口的关闭按钮事件
  const loginCloseBtn = loginBox.querySelector(".close");
  const registerCloseBtn = registerBox.querySelector(".close");

  loginCloseBtn.addEventListener("click", () => toggleDisplay(loginBox, false));
  registerCloseBtn.addEventListener("click", () => toggleDisplay(registerBox, false));


////注册和登录成功或错误提示框2s后收起效果
//  const targetNode = document.body;
//  const config = { childList: true, subtree: true };
//  const callback = function(mutationsList, observer) {
//      const flashMessages = document.querySelectorAll('.flash-message');
//      flashMessages.forEach(flashMessage => {
//        setTimeout(() => {
//                    flashMessage.remove();
//                }, 2000);
//    });
//
//
//    };
//    const observer = new MutationObserver(callback);
//    observer.observe(targetNode, config);



//    document.querySelector('.recipe-search-form').addEventListener('submit', function(event) {
//        event.preventDefault();
//        const query = document.querySelector('.recipe-search-input').value;
//        window.location.href = `/?search_query=${query}`;
//    });
  });



  

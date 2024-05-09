document.addEventListener("DOMContentLoaded", function() {
  // 登录和注册窗口的显示与隐藏控制
  const loginBox = document.querySelector("#login");
  const registerBox = document.querySelector("#register");

  // 显示登录窗口按钮
  const showLogins = document.querySelectorAll("#show_login");
  showLogins.forEach(btn => {
      btn.addEventListener("click", () => toggleDisplay(loginBox, true));
  });

  // 显示登录窗口按钮
  const showLogins2 = document.querySelectorAll("#openShi");
  showLogins2.forEach(btn => {
      btn.addEventListener("click", () => toggleDisplay(loginBox, true));
  });

  // 显示注册窗口按钮
  const showRegister = document.querySelector("#show_register");
  showRegister.addEventListener("click", () => toggleDisplay(registerBox, true));

   // 显示注册窗口按钮
   const showRegister2 = document.querySelector("#show_register2");
   showRegister2.addEventListener("click", () => toggleDisplay(registerBox, true));

  // 登录和注册窗口的关闭按钮事件
  const loginCloseBtn = loginBox.querySelector(".close");
  const registerCloseBtn = registerBox.querySelector(".close");

  loginCloseBtn.addEventListener("click", () => toggleDisplay(loginBox, false));
  registerCloseBtn.addEventListener("click", () => toggleDisplay(registerBox, false));

  // 登录表单提交事件
  const loginBt = document.querySelector("#login .btn_x");
  loginBt.addEventListener("click", handleLogin);

  // 注册表单提交事件
  const registerBt = document.querySelector("#register .btn_x");
  registerBt.addEventListener("click", handleRegister);

  // 用于显示或隐藏元素
  function toggleDisplay(element, show) {
      if (show) {
          element.classList.add("show");
      } else {
          element.classList.remove("show");
      }
  }

  // 处理登录逻辑
  function handleLogin(event) {
      const username = loginBox.querySelector('input[name="username"]').value;
      const password = loginBox.querySelector('input[name="password"]').value;

      if (!username || !password) {
          event.preventDefault();
          alert("Both username and password are required.");
          return false;
      }

      // 这里可以添加更多逻辑
  }

  // 处理注册逻辑
  function handleRegister(event) {
      const username = registerBox.querySelector('input[name="username"]').value;
      const nickname = registerBox.querySelector('input[name="nickname"]').value;
      const password = registerBox.querySelector('input[name="password"]').value;

      if (!username || !password|| !nickname) {
          event.preventDefault();
          alert("Both username, nickname and password are required for registration.");
          return false;
      }

      // 这里可以添加更多逻辑
  }

  // 淡出效果
  fadeOutMessages();
});

function fadeOutMessages() {
  const messages = document.querySelectorAll('.flash-message');
  setTimeout(() => {
      messages.forEach(message => {
          message.style.opacity = '0';
          setTimeout(() => {
              message.style.display = 'none';
          }, 600);
      });
  }, 4000);
}

document.addEventListener("DOMContentLoaded", function() {
    // Control the display and hiding of the login and register windows
    const loginBox = document.querySelector("#login");
    const registerBox = document.querySelector("#register");
  
    // Show login window button
    const showLogins = document.querySelectorAll("#show_login");
    showLogins.forEach(btn => {
        btn.addEventListener("click", () => toggleDisplay(loginBox, true));
    });
  
    // Show login window button
    const showLogins2 = document.querySelectorAll("#openShi");
    showLogins2.forEach(btn => {
        btn.addEventListener("click", () => toggleDisplay(loginBox, true));
    });
  
    // Show register window button
    const showRegister = document.querySelector("#show_register");
    showRegister.addEventListener("click", () => toggleDisplay(registerBox, true));
  
    // Show register window button
    const showRegister2 = document.querySelector("#show_register2");
    showRegister2.addEventListener("click", () => toggleDisplay(registerBox, true));
  
    // Close button events for the login and register windows
    const loginCloseBtn = loginBox.querySelector(".close");
    const registerCloseBtn = registerBox.querySelector(".close");
  
    loginCloseBtn.addEventListener("click", () => toggleDisplay(loginBox, false));
    registerCloseBtn.addEventListener("click", () => toggleDisplay(registerBox, false));
  
    // Login form submit event
    const loginBt = document.querySelector("#login .btn_x");
    loginBt.addEventListener("click", handleLogin);
  
    // Register form submit event
    const registerBt = document.querySelector("#register .btn_x");
    registerBt.addEventListener("click", handleRegister);
  
    // Function to show or hide elements
    function toggleDisplay(element, show) {
        if (show) {
            element.classList.add("show");
        } else {
            element.classList.remove("show");
        }
    }
  
    // Handle login logic
    function handleLogin(event) {
        const username = loginBox.querySelector('input[name="username"]').value;
        const password = loginBox.querySelector('input[name="password"]').value;
  
        if (!username || !password) {
            event.preventDefault();
            alert("Both username and password are required.");
            return false;
        }
  
        // More logic can be added here
    }
  
    // Handle register logic
    function handleRegister(event) {
        const username = registerBox.querySelector('input[name="username"]').value;
        const nickname = registerBox.querySelector('input[name="nickname"]').value;
        const password = registerBox.querySelector('input[name="password"]').value;
  
        if (!username || !password || !nickname) {
            event.preventDefault();
            alert("Username, nickname, and password are required for registration.");
            return false;
        }
  
        // More logic can be added here
    }
  
    // Fade out effect
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

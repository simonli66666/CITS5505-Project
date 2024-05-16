document.addEventListener("DOMContentLoaded", function() {
    // Controls for displaying and hiding login and registration boxes
    const loginBox = document.querySelector("#login");
    const registerBox = document.querySelector("#register");
  
    // Buttons to show the login box
    const showLogins = document.querySelectorAll("#show_login");
    showLogins.forEach(btn => {
        btn.addEventListener("click", () => toggleDisplay(loginBox, true));
    });
  
    // Another set of buttons to show the login box
    const showLogins2 = document.querySelectorAll("#openShi");
    showLogins2.forEach(btn => {
        btn.addEventListener("click", () => toggleDisplay(loginBox, true));
    });
  
    // Button to show the registration box
    const showRegister = document.querySelector("#show_register");
    showRegister.addEventListener("click", () => toggleDisplay(registerBox, true));
  
    // Another button to show the registration box
    const showRegister2 = document.querySelector("#show_register2");
    showRegister2.addEventListener("click", () => toggleDisplay(registerBox, true));
  
    // Close buttons for login and registration boxes
    const loginCloseBtn = loginBox.querySelector(".close");
    const registerCloseBtn = registerBox.querySelector(".close");
  
    loginCloseBtn.addEventListener("click", () => toggleDisplay(loginBox, false));
    registerCloseBtn.addEventListener("click", () => toggleDisplay(registerBox, false));
  
    // Event for login form submission
    const loginBt = document.querySelector("#login .btn_x");
    loginBt.addEventListener("click", handleLogin);
  
    // Event for registration form submission
    const registerBt = document.querySelector("#register .btn_x");
    registerBt.addEventListener("click", handleRegister);
  
    // Function to show or hide an element
    function toggleDisplay(element, show) {
        if (show) {
            element.classList.add("show");
        } else {
            element.classList.remove("show");
        }
    }
  
    // Function to handle login logic
    function handleLogin(event) {
        const username = loginBox.querySelector('input[name="username"]').value;
        const password = loginBox.querySelector('input[name="password"]').value;
  
        if (!username || !password) {
            event.preventDefault();
            alert("Both username and password are required.");
            return false;
        }
  
        // Additional logic can be added here
    }
  
    // Function to handle registration logic
    function handleRegister(event) {
        const username = registerBox.querySelector('input[name="username"]').value;
        const nickname = registerBox.querySelector('input[name="nickname"]').value;
        const password = registerBox.querySelector('input[name="password"]').value;
  
        if (!username || !password || !nickname) {
            event.preventDefault();
            alert("Username, nickname, and password are required for registration.");
            return false;
        }
  
        // Additional logic can be added here
    }
  
    // Function to fade out flash messages
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
  
console.log("Hello");
let button = document.getElementById("submit");
let alt1 = document.getElementById("username-alert-1");
let alt2 = document.getElementById("username-alert-2");
let alt3 = document.getElementById("password-alert-1");

button.disabled = true; // Disable the button initially

function usernameValidation() {
    let username = document.getElementById("username").value;
    let state = /^[a-zA-Z0-9_]{3,15}$/.test(username);
    if (!state) {
        alt1.style.display = "block"; // Show the alert message
        alt2.style.display = "none"; // Hide the alert message
        return false;
    }
    return true;
}
function pwdValidation() {
    let password = document.getElementById("password").value;
    if(password.length<8){
        alt3.style.display = "block"; // Show the alert message
        return false;
    }else{
    return true;
}}

let username = document.getElementById("username");
let password = document.getElementById("password");

username.addEventListener("input", function() {
    if(usernameValidation()){
        button.disabled = false;
        alt1.style.display = "none"; // Hide the alert message
        alt2.style.display = "none"; // Hide the alert message
    }
    else{
        button.disabled = true;
    }
    if (button.disabled == true){
        button.style.backgroundColor = "gray"; // Change the button color to gray
    }
    else{
        button.style.backgroundColor = "transparent"; // Change the button color to blue
    }
});
password.addEventListener("input", function() {
    if(pwdValidation()){
        button.disabled = false;
        alt3.style.display = "none"; // Hide the alert message
    }
    else{
        button.disabled = true;
    }
    if (button.disabled == true){
        button.style.backgroundColor = "gray"; // Change the button color to gray
    }
    else{
        button.style.backgroundColor = "transparent";
        console.log("Button enabled"); // Change the button color to blue
    }
});
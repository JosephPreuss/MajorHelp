document.addEventListener("DOMContentLoaded", function () {
    const togglePassword = document.getElementById("toggle-password");
    const passwordInput = document.getElementById("id_password"); // Django default password field ID

    togglePassword.addEventListener("click", function () {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            togglePassword.textContent = "Hide Password"; // Hide icon
        } else {
            passwordInput.type = "password";
            togglePassword.textContent = "Show Password"; // Show icon
        }
    });
});

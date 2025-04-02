document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const firstName = document.getElementById("first_name");
    const lastName = document.getElementById("last_name");
    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirm_password");
    const mobilePhone = document.getElementById("mobile_phone");

    form.addEventListener("submit", function (event) {
        let isValid = true;

        // Validate First Name
        if (firstName.value.trim() === "") {
            alert("First Name is required.");
            isValid = false;
        }

        // Validate Last Name
        if (lastName.value.trim() === "") {
            alert("Last Name is required.");
            isValid = false;
        }


        // Validate Password
        if (password.value.length < 6) {
            alert("Password must be at least 6 characters long.");
            isValid = false;
        }

        // Validate Confirm Password
        if (password.value !== confirmPassword.value) {
            alert("Passwords do not match.");
            isValid = false;
        }

    

        // Prevent form submission if validation fails
        if (!isValid) {
            event.preventDefault();
        }
    });
});
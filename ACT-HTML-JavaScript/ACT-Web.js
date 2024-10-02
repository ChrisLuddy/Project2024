// Wait for the DOM to fully load before executing the script
document.addEventListener("DOMContentLoaded", function () {
    // Global Functions 

    // Function to check if the user is logged in by checking the session
    function isLoggedIn() {
        // Sends a GET request to the server to verify if the session is valid
        return fetch("/api/check-session", { method: "GET" })
            .then(response => response.ok); // Returns true if the response is OK (status code 200)
    }

    // Function to retrieve the logged-in user's data from the server
    function getLoggedInUser() {
        // Sends a GET request to fetch user data
        return fetch("/api/user")
            .then(response => {
                // If the response is not OK, throw an error
                if (!response.ok) throw new Error('Failed to fetch user data');
                return response.json(); // Parse and return the user data as JSON
            });
    }

    // Redirects the user to the login page if they are not logged in
    function redirectIfNotLoggedIn() {
        return isLoggedIn().then(loggedIn => {
            // If the user is not logged in, redirect to the login page
            if (!loggedIn) {
                window.location.href = "ACT-Login.html";
            }
        });
    }

    // Homepage Script
    if (window.location.pathname.includes("ACT-Homepage.html")) {
        // Check if the user is logged in and update the display of the fund manager link accordingly
        isLoggedIn().then(loggedIn => {
            const fundManagerLink = document.querySelector('a[href="ACT-Fund-Manager-Welcome.html"]');
            // Show the fund manager link if logged in, otherwise hide it
            fundManagerLink.style.display = loggedIn ? "block" : "none";
        });
    }

    // Login Page Script 
    if (window.location.pathname.includes("ACT-Login.html")) {
        const loginForm = document.querySelector("form"); // Select the login form
        // Add event listener for form submission
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault(); // Prevent the default form submission behavior
            const email = document.getElementById("email").value; // Get the email value
            const password = document.getElementById("password").value; // Get the password value

            // Send a POST request to the backend for login
            fetch("/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json" // Set the content type for JSON data
                },
                body: JSON.stringify({ email, password }) // Send email and password as JSON
            })
            .then(response => {
                // If login failed, throw an error
                if (!response.ok) throw new Error('Login failed');
                return response.json(); // Parse the response JSON
            })
            .then(data => {
                // Redirect to the Fund Manager Welcome page upon successful login
                window.location.href = "ACT-Fund-Manager-Welcome.html";
            })
            .catch(error => {
                // Alert the user if the login credentials are invalid
                alert("Invalid login credentials.");
            });
        });
    }

    // Registration Page Script 
    if (window.location.pathname.includes("ACT-Register.html")) {
        const registrationForm = document.getElementById("registration-form"); // Select the registration form
        const usernameInput = document.getElementById("username"); // Select the username input
        const emailInput = document.getElementById("email"); // Select the email input
        const passwordInput = document.getElementById("password"); // Select the password input
        const passwordStrengthIndicator = document.getElementById("password-strength"); // Select password strength indicator

        // Add input event listener for username validation
        usernameInput.addEventListener("input", function () {
            const usernameError = document.getElementById("username-error"); // Select username error message
            // Show error if username length is less than 3 characters
            usernameError.style.display = usernameInput.value.length < 3 ? "block" : "none"; 
        });

        // Add input event listener for email validation
        emailInput.addEventListener("input", function () {
            const emailError = document.getElementById("email-error"); // Select email error message
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Regular expression for email validation
            // Show error if email is invalid
            emailError.style.display = !emailRegex.test(emailInput.value) ? "block" : "none"; 
        });

        // Add input event listener to assess password strength
        passwordInput.addEventListener("input", function () {
            const password = passwordInput.value; // Get the current password input
            let strength = ""; // Initialize strength variable
            // Determine password strength based on length
            if (password.length < 6) {
                strength = "Weak";
            } else if (password.length <= 10) {
                strength = "Moderate";
            } else {
                strength = "Strong";
            }
            // Display the strength of the password
            passwordStrengthIndicator.textContent = "Password Strength: " + strength;
        });

        // Add event listener for form submission
        registrationForm.addEventListener("submit", function (e) {
            e.preventDefault(); // Prevent default form submission behavior

            // Send a POST request to register the new user
            fetch("/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json" // Set the content type for JSON data
                },
                body: JSON.stringify({
                    username: usernameInput.value, // Send username
                    email: emailInput.value, // Send email
                    password: passwordInput.value // Send password
                })
            })
            .then(response => {
                // If registration failed, throw an error
                if (!response.ok) throw new Error('Registration failed');
                return response.json(); // Parse the response JSON
            })
            .then(data => {
                // Alert user upon successful registration and redirect to login page
                alert("Registration complete!");
                window.location.href = "ACT-Login.html";
            })
            .catch(error => {
                // Alert the user if registration fails
                alert("Registration failed: " + error.message);
            });
        });
    }

    // Fund Manager Welcome Page Script 
    if (window.location.pathname.includes("ACT-Fund-Manager-Welcome.html")) {
        // Check if the user is logged in, redirect if not
        redirectIfNotLoggedIn().then(() => {
            // Fetch user data after confirming user is logged in
            getLoggedInUser().then(userData => {
                // Check user role and redirect if unauthorized
                if (!userData || !(userData.role === 'Fund Manager' || userData.role === 'System Administrator')) {
                    window.location.href = "ACT-Login.html"; // Redirect to login if not authorized
                } else {
                    // Show the welcome container and display the user's name
                    const welcomeContainer = document.getElementById("welcome-container");
                    welcomeContainer.style.display = "block"; // Show the welcome container

                    const fundManagerName = document.getElementById("fund-manager-name"); // Select the name display element
                    fundManagerName.textContent = userData.name; // Set the user's name in the welcome message

                    // Fetch dashboard data from the backend
                    fetch("/api/dashboard")
                        .then(response => {
                            // If fetching dashboard data failed, throw an error
                            if (!response.ok) throw new Error('Failed to fetch dashboard data');
                            return response.json(); // Parse and return dashboard data
                        })
                        .then(data => {
                            // Display the retrieved dashboard data
                            document.getElementById("total-clients").textContent = data.totalClients;
                            document.getElementById("number-of-alerts").textContent = data.numberOfAlerts;
                            document.getElementById("recent-activities").textContent = data.recentActivities.join(", "); // Join recent activities with a comma
                        })
                        .catch(error => {
                            console.error(error); // Log any errors to the console
                            alert("Failed to load dashboard data."); // Alert user if fetching data fails
                        });
                }
            });
        });
    }

    // === Support Page Script ===
    if (window.location.pathname.includes("ACT-Support.html")) {
        const supportForm = document.querySelector("form"); // Select the support form
        // Add event listener for form submission
        supportForm.addEventListener("submit", function (e) {
            e.preventDefault(); // Prevent default form submission behavior
            const email = document.getElementById("email").value; // Get the email input value
            const message = document.getElementById("message").value; // Get the message input value

            // Send a POST request to the backend for support
            fetch("/api/support", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json" // Set the content type for JSON data
                },
                body: JSON.stringify({ email, message }) // Send email and message as JSON
            })
            .then(response => {
                // If support request failed, throw an error
                if (!response.ok) throw new Error('Support request failed');
                alert("Support message sent successfully."); // Alert user upon successful submission
                supportForm.reset(); // Reset the support form after submission
            })
            .catch(error => {
                // Alert the user if sending the support message fails
                alert("Failed to send support message: " + error.message);
            });
        });
    }
});

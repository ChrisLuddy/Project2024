document.addEventListener("DOMContentLoaded", function () {
    // Global Functions 

    // Function to check if the user is logged in by checking the session
    function isLoggedIn() {
        return fetch("/api/check-session", { method: "GET" })
            .then(response => response.ok); // Returns true if the response is OK
    }

    // Function to retrieve the logged-in user's data from the server
    function getLoggedInUser() {
        return fetch("/api/user")
            .then(response => {
                if (!response.ok) throw new Error('Failed to fetch user data');
                return response.json(); // Parse and return the user data as JSON
            });
    }

    // Redirects the user to the login page if they are not logged in
    function redirectIfNotLoggedIn() {
        return isLoggedIn().then(loggedIn => {
            if (!loggedIn) {
                window.location.href = "ACT-Login.html";
            }
        });
    }

    // Create the relaxed hue glow dynamically
    const mouseHue = document.createElement("div");
    mouseHue.id = "mouse-hue";
    document.body.appendChild(mouseHue);

    // Update glow position and hue on mousemove
    document.addEventListener("mousemove", (e) => {
        const x = Math.round((e.clientX / window.innerWidth) * 360);
        const y = Math.round((e.clientY / window.innerHeight) * 360);
        mouseHue.style.left = `${e.clientX}px`;
        mouseHue.style.top = `${e.clientY}px`;
        mouseHue.style.background = `radial-gradient(circle, hsla(${x}, 70%, 50%, 0.2), transparent 80%)`;
    });

    // Homepage Script
    if (window.location.pathname.includes("ACT-Homepage.html")) {
        isLoggedIn().then(loggedIn => {
            const fundManagerLink = document.querySelector('a[href="ACT-Fund-Manager-Welcome.html"]');
            fundManagerLink.style.display = loggedIn ? "block" : "none";
        });
    }

    // Login Page Script 
    if (window.location.pathname.includes("ACT-Login.html")) {
        const loginForm = document.querySelector("form");
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            fetch("/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            })
            .then(response => {
                if (!response.ok) throw new Error('Login failed');
                return response.json();
            })
            .then(data => {
                window.location.href = "ACT-Fund-Manager-Welcome.html";
            })
            .catch(error => {
                alert("Invalid login credentials.");
            });
        });
    }

    // Registration Page Script 
    if (window.location.pathname.includes("ACT-Register.html")) {
        const registrationForm = document.getElementById("registration-form");
        const usernameInput = document.getElementById("username");
        const emailInput = document.getElementById("email");
        const passwordInput = document.getElementById("password");
        const passwordStrengthIndicator = document.getElementById("password-strength");

        usernameInput.addEventListener("input", function () {
            const usernameError = document.getElementById("username-error");
            usernameError.style.display = usernameInput.value.length < 3 ? "block" : "none"; 
        });

        emailInput.addEventListener("input", function () {
            const emailError = document.getElementById("email-error");
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            emailError.style.display = !emailRegex.test(emailInput.value) ? "block" : "none"; 
        });

        passwordInput.addEventListener("input", function () {
            const password = passwordInput.value;
            let strength = "";
            if (password.length < 6) {
                strength = "Weak";
            } else if (password.length <= 10) {
                strength = "Moderate";
            } else {
                strength = "Strong";
            }
            passwordStrengthIndicator.textContent = "Password Strength: " + strength;
        });

        registrationForm.addEventListener("submit", function (e) {
            e.preventDefault();

            fetch("/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: usernameInput.value,
                    email: emailInput.value,
                    password: passwordInput.value
                })
            })
            .then(response => {
                if (!response.ok) throw new Error('Registration failed');
                return response.json();
            })
            .then(data => {
                alert("Registration complete!");
                window.location.href = "ACT-Login.html";
            })
            .catch(error => {
                alert("Registration failed: " + error.message);
            });
        });
    }

    // Fund Manager Welcome Page Script 
    if (window.location.pathname.includes("ACT-Fund-Manager-Welcome.html")) {
        redirectIfNotLoggedIn().then(() => {
            getLoggedInUser().then(userData => {
                if (!userData || !(userData.role === 'Fund Manager' || userData.role === 'System Administrator')) {
                    window.location.href = "ACT-Login.html";
                } else {
                    const welcomeContainer = document.getElementById("welcome-container");
                    welcomeContainer.style.display = "block";

                    const fundManagerName = document.getElementById("fund-manager-name");
                    fundManagerName.textContent = userData.name;

                    fetch("/api/dashboard")
                        .then(response => {
                            if (!response.ok) throw new Error('Failed to fetch dashboard data');
                            return response.json();
                        })
                        .then(data => {
                            document.getElementById("total-clients").textContent = data.totalClients;
                            document.getElementById("number-of-alerts").textContent = data.numberOfAlerts;
                            document.getElementById("recent-activities").textContent = data.recentActivities.join(", ");
                        })
                        .catch(error => {
                            console.error(error);
                            alert("Failed to load dashboard data.");
                        });
                }
            });
        });
    }

    // === Support Page Script ===
    if (window.location.pathname.includes("ACT-Support.html")) {
        const supportForm = document.querySelector("form");
        supportForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const email = document.getElementById("email").value;
            const message = document.getElementById("message").value;

            fetch("/api/support", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, message })
            })
            .then(response => {
                if (!response.ok) throw new Error('Support request failed');
                alert("Support message sent successfully.");
                supportForm.reset();
            })
            .catch(error => {
                alert("Failed to send support message: " + error.message);
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const numDots = 30; // Number of neon dots
    const dots = [];
    let mouseX = 0, mouseY = 0;

    // Create dots and append them to the body
    for (let i = 0; i < numDots; i++) {
        const dot = document.createElement('div');
        dot.className = 'neon-dot'; // Add a class for styling
        document.body.appendChild(dot);
        dots.push(dot);
    }

    // Function to move dots in a trailing effect
    function moveDots() {
        let nextX = mouseX, nextY = mouseY;

        // Move each dot towards the mouse position with easing
        dots.forEach((dot) => {
            const currentX = dot.style.left ? parseFloat(dot.style.left) : 0;
            const currentY = dot.style.top ? parseFloat(dot.style.top) : 0;

            // Update the position of the dot
            dot.style.left = `${nextX}px`;
            dot.style.top = `${nextY}px`;

            // Calculate the next position with easing for smooth movement
            nextX += (currentX - nextX) * 0.3;
            nextY += (currentY - nextY) * 0.3;
        });

        requestAnimationFrame(moveDots); // Continue the animation
    }

    // Track mouse movement
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;  // Get horizontal mouse position
        mouseY = e.clientY;  // Get vertical mouse position
    });

    moveDots(); // Start the dot animation
});


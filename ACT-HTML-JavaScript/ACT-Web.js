// Wait for the DOM to fully load before running scripts
document.addEventListener("DOMContentLoaded", function () {
    // Global Functions 

    // Function to check if the user is logged in by verifying session status from the backend
    function isLoggedIn() {
        return fetch("/api/check-session", { method: "GET" })
            .then(response => response.ok); // Returns true if session is active (HTTP 200 response)
    }

    // Function to retrieve current logged-in user's details from the backend
    function getLoggedInUser() {
        return fetch("/api/user")
            .then(response => {
                if (!response.ok) throw new Error('Failed to fetch user data'); // Handle errors in fetching
                return response.json(); // Parse and return JSON data if successful
            });
    }

    // Function to handle Firebase login, returning user token after authentication
    function handleFirebaseLogin(email, password) {
        return firebase.auth().signInWithEmailAndPassword(email, password)
            .then(userCredential => {
                return userCredential.user.getIdToken(); // Retrieve user token after login
            })
            .then(token => {
                return fetch("/api/login", { // Send token to backend for additional validation
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}` // Attach token for authorization
                    }
                });
            });
    }

    // Redirects the user to the login page if not logged in
    function redirectIfNotLoggedIn() {
        return isLoggedIn().then(loggedIn => {
            if (!loggedIn) {
                window.location.href = "ACT-Login.html"; // Redirect to login page if not logged in
            }
        });
    }

    // Homepage Script to check and display fund manager link only if logged in
    if (window.location.pathname.includes("ACT-Homepage.html")) {
        isLoggedIn().then(loggedIn => {
            const fundManagerLink = document.querySelector('a[href="ACT-Fund-Manager-Welcome.html"]');
            fundManagerLink.style.display = loggedIn ? "block" : "none"; // Show or hide link based on login status
        });
    }

    // Login Page Script for handling form submission and Firebase login
    if (window.location.pathname.includes("ACT-Login.html")) {
        const loginForm = document.querySelector("form"); // Select the login form
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault(); // Prevent default form submission behavior
            const email = document.getElementById("email").value; // Get email value
            const password = document.getElementById("password").value; // Get password value

            // Perform Firebase login and handle response
            handleFirebaseLogin(email, password)
                .then(response => {
                    if (!response.ok) throw new Error('Login failed'); // Throw error if login fails
                    return response.json(); // Parse JSON response if successful
                })
                .then(() => {
                    window.location.href = "ACT-Fund-Manager-Welcome.html"; // Redirect after successful login
                })
                .catch(error => {
                    alert("Invalid login credentials."); // Alert user on login failure
                });
        });
    }

    // Registration Page Script with form validation and user registration
    if (window.location.pathname.includes("ACT-Register.html")) {
        const registrationForm = document.getElementById("registration-form"); // Select registration form
        const usernameInput = document.getElementById("username"); // Select username input
        const emailInput = document.getElementById("email"); // Select email input
        const passwordInput = document.getElementById("password"); // Select password input
        const passwordStrengthIndicator = document.getElementById("password-strength"); // Select password strength indicator

        // Check username validity and show error if username is too short
        usernameInput.addEventListener("input", function () {
            const usernameError = document.getElementById("username-error");
            usernameError.style.display = usernameInput.value.length < 3 ? "block" : "none"; 
        });

        // Check email validity and show error if format is incorrect
        emailInput.addEventListener("input", function () {
            const emailError = document.getElementById("email-error");
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Basic email regex validation
            emailError.style.display = !emailRegex.test(emailInput.value) ? "block" : "none"; 
        });

        // Check password strength and display appropriate message
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
            passwordStrengthIndicator.textContent = "Password Strength: " + strength; // Display password strength
        });

        // Handle registration form submission
        registrationForm.addEventListener("submit", function (e) {
            e.preventDefault();

            // Send registration details to backend
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
                if (!response.ok) throw new Error('Registration failed'); // Handle registration errors
                return response.json();
            })
            .then(() => {
                alert("Registration complete!"); // Notify user of successful registration
                window.location.href = "ACT-Login.html"; // Redirect to login page
            })
            .catch(error => {
                alert("Registration failed: " + error.message); // Display error message on failure
            });
        });
    }

    // Fund Manager Welcome Page Script for displaying user data and dashboard info
    if (window.location.pathname.includes("ACT-Fund-Manager-Welcome.html")) {
        redirectIfNotLoggedIn().then(() => { // Ensure user is logged in before fetching data
            getLoggedInUser().then(userData => {
                if (!userData || !(userData.role === 'Fund Manager' || userData.role === 'System Administrator')) {
                    window.location.href = "ACT-Login.html"; // Redirect unauthorized users
                } else {
                    const welcomeContainer = document.getElementById("welcome-container"); // Show welcome container
                    welcomeContainer.style.display = "block";
                    const fundManagerName = document.getElementById("fund-manager-name");
                    fundManagerName.textContent = userData.name; // Display fund manager's name

                    // Fetch and display dashboard data
                    fetch("/api/dashboard")
                        .then(response => {
                            if (!response.ok) throw new Error('Failed to fetch dashboard data');
                            return response.json();
                        })
                        .then(data => {
                            document.getElementById("total-clients").textContent = data.totalClients; // Show client count
                            document.getElementById("number-of-alerts").textContent = data.numberOfAlerts; // Show alerts
                            document.getElementById("recent-activities").textContent = data.recentActivities.join(", "); // List recent activities
                        })
                        .catch(error => {
                            console.error(error);
                            alert("Failed to load dashboard data."); // Alert user on data fetch error
                        });
                }
            });
        });
    }

    // Fund Manager Page Script for displaying managed funds and client list
    if (window.location.pathname.includes("ACT-Fund-Manager.html")) {
        redirectIfNotLoggedIn().then(() => { // Ensure login
            getLoggedInUser().then(userData => {
                if (userData.role === 'Fund Manager') { // Check user role
                    fetch("/api/fund-manager-data") // Fetch manager data from backend
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById("manager-info").textContent = `Managed Funds: ${data.managedFunds}`; // Show funds
                            document.getElementById("client-list").textContent = data.clientList.join(", "); // Show clients
                        })
                        .catch(error => {
                            alert("Failed to fetch fund manager data: " + error.message); // Handle errors
                        });
                } else {
                    window.location.href = "ACT-Login.html"; // Redirect unauthorized users
                }
            });
        });
    }

    // AI Predictions Page Script for retrieving and displaying AI predictions
    if (window.location.pathname.includes("ACT-AI-Predictions.html")) {
        redirectIfNotLoggedIn().then(() => { // Ensure login
            fetch("/api/ai-predictions") // Fetch predictions data
                .then(response => response.json())
                .then(data => {
                    document.getElementById("ai-predictions").textContent = data.predictions.join(", "); // Display predictions
                })
                .catch(error => {
                    alert("Failed to fetch AI predictions: " + error.message); // Handle errors
                });
        });
    }

    // Support Page Script for handling support message form submission
    if (window.location.pathname.includes("ACT-Support.html")) {
        const supportForm = document.querySelector("form");
        supportForm.addEventListener("submit", function (e) {
            e.preventDefault(); // Prevent default submission
            const email = document.getElementById("email").value; // Get email
            const message = document.getElementById("message").value; // Get message

            // Send support request to backend
            fetch("/api/support", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, message })
            })
            .then(response => {
                if (!response.ok) throw new Error('Support request failed'); // Handle errors
                alert("Support message sent successfully."); // Success notification
                supportForm.reset(); // Reset form fields
            })
            .catch(error => {
                alert("Failed to send support message: " + error.message); // Error notification
            });
        });
    }
});

// Reports Page Script
if (window.location.pathname.includes("ACT-Reports.html")) {
        
    // Function to dynamically add stocks and cryptocurrencies to the page
    function loadFinancialData(stocks, cryptocurrencies) {
        const stockList = document.getElementById("stock-list"); // Select stock list element
        const cryptoList = document.getElementById("crypto-list"); // Select crypto list element

        // Populate stock list
        stocks.forEach(stock => {
            const listItem = document.createElement("li"); // Create list item for each stock
            listItem.textContent = `${stock.name} - ${stock.quantity} shares at $${stock.price}`; // Set text
            stockList.appendChild(listItem); // Add list item to stock list
        });

        // Populate cryptocurrency list
        cryptocurrencies.forEach(crypto => {
            const listItem = document.createElement("li"); // Create list item for each crypto
            listItem.textContent = `${crypto.name} - ${crypto.quantity} units at $${crypto.price}`; // Set text
            cryptoList.appendChild(listItem); // Add list item to crypto list
        });
    }


    // Dynamically retrieve stocks and cryptocurrencies in order to set up price system alerts
    {
        // Function to dynamically load assets from the backend and populate dropdowns
        async function loadAssets() {
            try {
                const response = await fetch('/api/assets'); // Endpoint to get saved assets
                const assets = await response.json();
                const assetDropdown = document.getElementById('asset');
                assets.forEach(asset => {
                    const option = document.createElement('option');
                    option.value = asset.symbol;
                    option.textContent = `${asset.name} (${asset.symbol})`;
                    assetDropdown.appendChild(option);
                });
            } catch (error) {
                console.error('Error loading assets:', error);
            }
        }
    
        // Function to fetch client assets and display alerts on the page
        async function loadClientAssets() {
            try {
                const response = await fetch('/api/client-assets'); // Endpoint for client-specific assets
                const clientAssets = await response.json();
                const alertList = document.getElementById('alert-list');
                alertList.innerHTML = ''; // Clear existing alerts
                clientAssets.forEach(asset => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${asset.name} (${asset.symbol}): ${asset.alertMessage}`;
                    alertList.appendChild(listItem);
                });
            } catch (error) {
                console.error('Error loading client assets:', error);
            }
        }
    
        // Simulated backend data for stocks and cryptocurrencies
        const stocks = [
            { name: "Apple", quantity: 10, price: 150 },
            { name: "Tesla", quantity: 5, price: 700 },
        ];
    
        const cryptocurrencies = [
            { name: "Bitcoin", quantity: 0.5, price: 45000 },
            { name: "Ethereum", quantity: 2, price: 3000 },
        ];
    
        // Function to load financial data onto the page
        function loadFinancialData(stocks, cryptocurrencies) {
            const stockList = document.getElementById("stock-list");
            const cryptoList = document.getElementById("crypto-list");
    
            stocks.forEach(stock => {
                const stockItem = document.createElement("li");
                stockItem.textContent = `${stock.name}: ${stock.quantity} shares at $${stock.price}`;
                stockList.appendChild(stockItem);
            });
    
            cryptocurrencies.forEach(crypto => {
                const cryptoItem = document.createElement("li");
                cryptoItem.textContent = `${crypto.name}: ${crypto.quantity} units at $${crypto.price}`;
                cryptoList.appendChild(cryptoItem);
            });
        }
    
        // Function to download financial report as PDF
        document.getElementById("download-pdf").addEventListener("click", function () {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            doc.text("Financial Report", 10, 10);
    
            doc.text("Stocks:", 10, 20);
            stocks.forEach((stock, index) => {
                doc.text(`${stock.name}: ${stock.quantity} shares at $${stock.price}`, 10, 30 + index * 10);
            });
    
            doc.text("Cryptocurrencies:", 10, 30 + stocks.length * 10);
            cryptocurrencies.forEach((crypto, index) => {
                doc.text(`${crypto.name}: ${crypto.quantity} units at $${crypto.price}`, 10, 40 + stocks.length * 10 + index * 10);
            });
    
            doc.save("financial-report.pdf");
        });
    
        // Function to download financial report as CSV
        document.getElementById("download-csv").addEventListener("click", function () {
            let csvContent = "data:text/csv;charset=utf-8,";
            csvContent += "Type,Name,Quantity,Price\n";
    
            stocks.forEach(stock => {
                csvContent += `Stock,${stock.name},${stock.quantity},${stock.price}\n`;
            });
    
            cryptocurrencies.forEach(crypto => {
                csvContent += `Crypto,${crypto.name},${crypto.quantity},${crypto.price}\n`;
            });
    
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "financial-report.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    
        // Initialize by loading assets and financial data onto the page
        loadAssets();
        loadFinancialData(stocks, cryptocurrencies);
    
        // Load client-specific alerts on relevant pages
        if (window.location.pathname.includes("ACT-Fund-Manager.html") || window.location.pathname.includes("ACT-AI-Predictions.html")) {
            loadClientAssets();
        }
    };
}


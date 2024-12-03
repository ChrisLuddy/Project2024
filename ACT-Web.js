// Base API URL
// const BASE_URL = "http://127.0.0.1:8000/api";

const BASE_URL = "http://161.35.38.50:8000/api";
let accessToken = ""; // Store JWT token after login

// Firebase Initialization
(async function initializeFirebase() {
    // Dynamically fetch Firebase configuration 
    const firebaseConfig = await fetch("/path/to/your/firebase-config.json")
        .then(response => {
            if (!response.ok) throw new Error("Failed to load Firebase configuration");
            return response.json();
        })
        .catch(error => {
            console.error("Firebase initialization error:", error.message);
        });

    // Initialize Firebase with fetched configuration
    if (firebaseConfig) {
        import("https://www.gstatic.com/firebasejs/9.6.10/firebase-app.js")
            .then(({ initializeApp }) => {
                const app = initializeApp(firebaseConfig);
                console.log("Firebase Initialized:", app);
            })
            .catch(error => console.error("Error importing Firebase App:", error.message));
    }
})();

// Helper function to set headers
function getHeaders(authRequired = true) {
    const headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    };
    if (authRequired && accessToken) {
        headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return headers;
}

// Authentication Functions

// Handle Login
function handleLogin(username, password) {
    return fetch(`${BASE_URL}/token/`, {
        method: "POST",
        headers: getHeaders(false),
        body: JSON.stringify({ username, password }),
    })
        .then(response => {
            if (!response.ok) throw new Error("Invalid login credentials");
            return response.json();
        })
        .then(data => {
            accessToken = data.access;
            return data;
        });
}

// Handle Registration
function handleRegistration(username, password, role) {
    return fetch(`${BASE_URL}/register/`, {
        method: "POST",
        headers: getHeaders(false),
        body: JSON.stringify({ username, password, role }), // Include role
    })
        .then(response => {
            if (!response.ok) throw new Error("Registration failed");
            return response.json();
        });
}

// Fetch Functions

// Fetch Yahoo News
function fetchYahooNews(tickers = "", type = "ALL") {
    const queryParams = new URLSearchParams({ tickers, type });
    return fetch(`${BASE_URL}/yahoo-news/?${queryParams.toString()}`, {
        method: "GET",
        headers: getHeaders(),
    }).then(response => {
        if (!response.ok) throw new Error("Failed to fetch Yahoo News");
        return response.json();
    });
}

// Fetch User Details
function fetchUserDetails() {
    return fetch(`${BASE_URL}/user/`, {
        method: "GET",
        headers: getHeaders(),
    }).then(response => {
        if (!response.ok) throw new Error("Failed to fetch user details");
        return response.json();
    });
}

// Fetch Assets
function fetchAssets() {
    return fetch(`${BASE_URL}/assets/`, {
        method: "GET",
        headers: getHeaders(),
    }).then(response => {
        if (!response.ok) throw new Error("Failed to fetch assets");
        return response.json();
    });
}

// Action Functions

// Handle Purchase
function makePurchase(stocks, cryptos) {
    return fetch(`${BASE_URL}/purchase/`, {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify({ stocks, cryptos }),
    }).then(response => {
        if (!response.ok) throw new Error("Failed to complete purchase");
        return response.json();
    });
}

// DOM Manipulation

// Initialize Login Page
function initLoginPage() {
    const loginForm = document.querySelector("form");
    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        handleLogin(username, password)
            .then(() => {
                alert("Login successful!");
                window.location.href = "ACT-Fund-Manager-Welcome.html";
            })
            .catch(error => alert(error.message));
    });
}

// Initialize Registration Page
function initRegistrationPage() {
    const registrationForm = document.getElementById("registration-form");
    registrationForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const username = document.getElementById("username").value; // Username
        const password = document.getElementById("password").value; // Password
        const role = document.getElementById("role").value; // Role from dropdown or input

        handleRegistration(username, password, role) // Include role in the registration payload
            .then(() => {
                alert("Registration successful!");
                window.location.href = "ACT-Login.html"; // Redirect to login page
            })
            .catch(error => alert(error.message));
    });
}

// Function to check the performance and return a status label
function getPerformanceStatus(change) {
    if (change < 0) {
        return "poor";
    } else {
        return "good";
    }
}

// Example usage
let netChange1 = -10; // Example negative change
let netChange2 = 15;  // Example positive change

console.log(`The performance is ${getPerformanceStatus(netChange1)} for change: ${netChange1}%`);
console.log(`The performance is ${getPerformanceStatus(netChange2)} for change: ${netChange2}%`);

// Function to apply this to elements on a webpage
function updateTablePerformance() {
    // Select all table rows that need checking
    const rows = document.querySelectorAll('.trade-table tbody tr');

    rows.forEach(row => {
        const changeCell = row.querySelector('td:nth-child(5)'); // Assuming the 5th cell contains the change %
        const performanceCell = row.querySelector('td:last-child'); // Last cell for status label

        // Parse the change as a float (assumes % sign is not present)
        const change = parseFloat(changeCell.textContent);

        // Get performance status and update the performance cell
        const status = getPerformanceStatus(change);
        performanceCell.textContent = status.charAt(0).toUpperCase() + status.slice(1); // Capitalize first letter

        // Add a class to color-code the cell
        performanceCell.className = `status ${status}`;
    });
}

// Call the function when the page is loaded
window.onload = updateTablePerformance;

// Function to update the price and calculate the change
function updatePrice(rowSelector, newPrice) {
    // Select the specific row
    const row = document.querySelector(rowSelector);

    // Select the cells for entry price and current price
    const entryPriceCell = row.querySelector('td:nth-child(3)');
    const currentPriceCell = row.querySelector('td:nth-child(4)');
    const changeCell = row.querySelector('td:nth-child(5)');
    const statusCell = row.querySelector('td:nth-child(6)');

    // Get the entry price as a number
    const entryPrice = parseFloat(entryPriceCell.textContent.replace(/[^0-9.-]+/g, ''));
    
    // Update the current price cell with the new price
    currentPriceCell.textContent = `$${newPrice.toFixed(2)}`;

    // Calculate the change percentage
    const changePercentage = ((newPrice - entryPrice) / entryPrice) * 100;
    changeCell.textContent = `${changePercentage.toFixed(2)}%`;

    // Determine the status based on the change percentage
    const status = changePercentage < 0 ? "poor" : "good";
    statusCell.textContent = status.charAt(0).toUpperCase() + status.slice(1);
    statusCell.className = `status ${status}`;
}

// Example usage to update the first row in the table with a new price
updatePrice('.trade-table tbody tr', 23000);

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

// Support Page Script
if (window.location.pathname.includes("ACT-Support.html")) {
    const supportForm = document.querySelector("form");
    supportForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const query = document.getElementById("query").value;
        const email = document.getElementById("email").value;

        sendSupportQuery(query, email)
            .then(() => alert("Your query has been sent!"))
            .catch(error => alert(error.message));
    });
}

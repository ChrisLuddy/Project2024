// Base API URL
// const BASE_URL = "http://161.35.38.50:8000/api";

const BASE_URL = "http://161.35.38.50:8000/api";
let accessToken = ""; // Store JWT token after login

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
function handleLogin(username, email, password) {
    return fetch(`${BASE_URL}/token/`, {
        method: "POST",
        headers: getHeaders(false),
        body: JSON.stringify({ username, email, password }),
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
function handleRegistration(username, email, password, role) {
    return fetch(`${BASE_URL}/register/`, {
        method: "POST",
        headers: getHeaders(false),
        body: JSON.stringify({ username, email, password, role }), // Include role
    })
        .then(response => {
            if (!response.ok) throw new Error("Registration failed");
            return response.json();
        });
}

// Google SignIn Handling
async function onGoogleSignIn(googleUser) {
    const profile = googleUser.getBasicProfile();
    const idToken = googleUser.getAuthResponse().id_token; // Get Google ID token
    const username = profile.getName();
    const email = profile.getEmail();

    // Prompt user to select a role
    const role = prompt("Please choose your role: 'fund_admin', 'fund_manager', or 'system_admin'");

    if (!role || !['fund_admin', 'fund_manager', 'system_admin'].includes(role)) {
        alert("Invalid role selected. Please try again.");
        return; // Exit if the role is invalid
    }

    try {
        // Send ID token and role to the backend
        const response = await fetch(`${BASE_URL}/google-auth/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ id_token: idToken, role }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Google authentication failed.");
        }

        const data = await response.json();
        accessToken = data.access; // Store JWT access token

        // Update navigation links and redirect
        updateNavigationLinks();
        alert("Sign-in successful!");
        if (data.user.role === 'fund_admin') {
            window.location.href = "ACT-Portfolio.html"; 
        } else if (['fund_manager', 'system_admin'].includes(data.user.role)) {
            window.location.href = "ACT-Fund-Manager-Welcome.html";
        } else {
            window.location.href = "ACT-Portfolio.html"; // Default fallback
        }
    } catch (error) {
        console.error("Error during Google Sign-In:", error);
        alert(error.message);
    }
}

// Google Sign-In Button Initialization
function googleInit() {
    google.accounts.id.initialize({
        client_id: 'GOOGLE_CLIENT_ID', 
        callback: onGoogleSignIn,
    });

    google.accounts.id.renderButton(
        document.getElementById("google-login-btn"),
        { 
            theme: "outline", 
            size: "large", 
            shape: "pill" 
        }
    );
}

document.addEventListener("DOMContentLoaded", function () {
    googleInit();
});



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

// Function to update navigation links based on login status
function updateNavigationLinks() {
    const navLinks = document.querySelectorAll('#nav-links .auth-required');
    if (accessToken) {
        // User is logged in, show all links
        navLinks.forEach(link => link.style.display = 'list-item');
    } else {
        // User is logged out, hide auth-required links
        navLinks.forEach(link => link.style.display = 'none');
    }
}

// DOM Manipulation

// Initialize Login Page
function initLoginPage() {
    const loginForm = document.querySelector("form");
    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        handleLogin(username, email, password)
            .then(() => {
                alert("Login successful!");
                fetchUserDetails().then(user => {
                    if (user.role === 'fund_admin') {
                        window.location.href = "ACT-Portfolio.html"; 
                    } else if (user.role === 'system_admin' || user.role === 'fund_manager') {
                        window.location.href = "ACT-Fund-Manager-Welcome.html"; 
                    }
                }).catch(error => {
                    console.error("Error fetching user details:", error);
                    alert("An error occurred while determining user role. Redirecting to default page.");
                    window.location.href = "ACT-Portfolio.html"; 
                });
            })
            .catch(error => alert(error.message));
    });
}


// Initialize Registration Page
function initRegistrationPage() {
    const registrationForm = document.getElementById("registration-form");
    registrationForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const username = document.getElementById("username").value; 
        const email = document.getElementById("email").value; 
        const password = document.getElementById("password").value;
        const role = document.getElementById("role").value; 

        handleRegistration(username, email, password, role) 
            .then(() => {
                alert("Registration successful!");
                window.location.href = "ACT-Login.html"; // Redirect to login page
            })
            .catch(error => alert(error.message));
    });
}

// Initialize Yahoo News Page
function initYahooNewsPage() {
    fetchYahooNews("AAPL", "ALL")
        .then(data => {
            const newsContainer = document.getElementById("news-container");
            newsContainer.innerHTML = data.body
                .map(
                    article => `
                <div class="news-item">
                    <img src="${article.img}" alt="${article.title}">
                    <h3>${article.title}</h3>
                    <p>${article.text}</p>
                    <a href="${article.url}" target="_blank">Read more</a>
                </div>
            `
                )
                .join("");
        })
        .catch(error => alert("Error fetching news: " + error.message));
}

// Initialize Purchase Page
function initPurchasePage() {
    const purchaseForm = document.getElementById("purchase-form");
    
    // Add the new functionality (which is the e.preventDefault())
    purchaseForm.addEventListener("submit", function (e) {
        e.preventDefault();
        
        // Add the current logic of getting stocks and cryptos
        const stocks = document.getElementById("stocks").value.split(",");
        const cryptos = document.getElementById("cryptos").value.split(",");

        makePurchase(stocks, cryptos)
            .then(data => {
                alert("Purchase successful!");
                console.log("Purchase Summary:", data);
            })
            .catch(error => alert("Error making purchase: " + error.message));
    });
}


// Fetch Yahoo News
function fetchYahooNews(tickers = "", type = "ALL") {
    const queryParams = new URLSearchParams({ tickers, type });
    return fetch(`${BASE_URL}/yahoo-news/?${queryParams.toString()}`, {
        method: "GET",
        headers: getHeaders(false), // Authorization not required
    }).then(response => {
        if (!response.ok) throw new Error("Failed to fetch Yahoo News");
        return response.json();
    });
}

function updateNews() {
    fetchYahooNews("AAPL", "ALL")
        .then(data => {
            const newsContainer = document.getElementById("news-container");
            newsContainer.innerHTML = data.body
                .map(article => {
                    // Ensure date is formatted properly
                    const publishedDate = new Date(article.date || article.pubDate || Date.now()).toLocaleString();

                    return `
                        <div class="news-item">
                            <img src="${article.img || ''}" alt="${article.title}" />
                            <h3>${article.title} <small>(${publishedDate})</small></h3>
                            <p>${article.text}</p>
                            <a href="${article.url}" target="_blank">Read more</a>
                        </div>
                    `;
                })
                .join("");
        })
        .catch(error => alert("Error fetching news: " + error.message));
}

function initYahooNewsPage() {
    // Initial news load
    updateNews();

    // Add event listener for the refresh button
    const refreshButton = document.getElementById("refresh-news-button");
    refreshButton.addEventListener("click", () => {
        updateNews();
    });
}

// Function to update Fund Manager's name and dashboard data on Fund Manager Welcome Page
function updateFundManagerWelcome() {
    // Fetch user details (including fund manager's name)
    fetchUserDetails()
        .then(user => {
            // Update the welcome message with the fund manager's name
            document.getElementById('fund-manager-name').textContent = user.username; // Assuming username is the fund manager's name

            fetchDashboardData(user.username)
                .then(data => {
                    // Update the dashboard metrics dynamically
                    document.getElementById('total-clients').textContent = data.totalClients;
                    document.getElementById('number-of-alerts').textContent = data.numberOfAlerts;
                    document.getElementById('recent-activities').textContent = data.recentActivities;
                    
                    // Make the welcome page visible after data is loaded
                    document.getElementById('welcome-container').style.display = 'block';
                })
                .catch(error => {
                    console.error('Error fetching dashboard data:', error);
                });
        })
        .catch(error => {
            console.error('Error fetching user details:', error);
        });
}

// Function to fetch dashboard data (Total Clients, Number of Alerts, Recent Activities)
function fetchDashboardData(fundManagerUsername) {
    return fetch(`${BASE_URL}/dashboard/${fundManagerUsername}/`, {
        method: "GET",
        headers: getHeaders(),
    })
        .then(response => {
            if (!response.ok) throw new Error("Failed to fetch dashboard data");
            return response.json();
        })
        .then(data => {
            return {
                totalClients: data.totalClients, 
                numberOfAlerts: data.numberOfAlerts, 
                recentActivities: data.recentActivities, 
            };
        });
}


// Main Initialization
document.addEventListener("DOMContentLoaded", () => { 
    const path = window.location.pathname;

    if (path.includes("ACT-Login.html")) {
        initLoginPage();
    } else if (path.includes("ACT-Register.html")) {
        initRegistrationPage();
    } else if (path.includes("ACT-Yahoo-News.html")) {
        initYahooNewsPage();
    } else if (path.includes("ACT-Purchase.html")) {
        initPurchasePage();
    } else  if (window.location.pathname.includes("ACT-Fund-Manager-Welcome.html")) {
        updateFundManagerWelcome();
    }


    updateNavigationLinks();

    if (window.location.pathname.includes("ACT-Login.html")) {
        const loginForm = document.querySelector("form");
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const username = document.getElementById("username").value;
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            handleLogin(username, email, password)
                .then(() => {
                    alert("Login successful!");
                    updateNavigationLinks(); // Update links after login
                    fetchUserDetails().then(user => {
                        if (user.role === 'fund_admin') {
                            window.location.href = "ACT-Portfolio.html"; // Redirect to Portfolio page
                        } else if (user.role === 'system_admin' || user.role === 'fund_manager') {
                            window.location.href = "ACT-Fund-Manager-Welcome.html"; // Redirect to Fund Manager Welcome page
                        }
                    }).catch(error => {
                        console.error("Error fetching user details:", error);
                        window.location.href = "ACT-Portfolio.html"; // Default redirect in case of error
                    });
                })
                .catch(error => alert(error.message));
        });
    }

    const stars = document.querySelectorAll("#star-rating .star");
    const selectedRating = document.getElementById("selected-rating");

    stars.forEach(star => {
        star.addEventListener("click", () => {
            const ratingValue = star.dataset.value;

            // Update the selected rating text
            selectedRating.textContent = `Selected Rating: ${ratingValue}`;

            // Highlight the selected stars
            stars.forEach(s => {
                s.style.color = s.dataset.value <= ratingValue ? "gold" : "black";
            });
        });
    });

    function buyStocks() {
        const stocksSelected = document.getElementById('stocks').selectedOptions;
        const quantity = document.getElementById('quantity').value;
    
        if (stocksSelected.length > 10) {
            alert("You can select up to 10 stocks.");
            return;
        }
    
        if (quantity < 1 || quantity > 10) {
            alert("Quantity must be between 1 and 10.");
            return;
        }
    
        // Logic for purchasing stocks
        let purchaseSummary = "Purchased Stocks: ";
        for (let i = 0; i < stocksSelected.length; i++) {
            purchaseSummary += stocksSelected[i].value + " (Qty: " + quantity + "), ";
        }
        document.getElementById("purchase-summary").innerText = purchaseSummary;
    
        // Make the API call to process the purchase
        const stocks = Array.from(stocksSelected).map(stock => stock.value);
        makePurchase(stocks, [])
            .then(data => {
                alert("Purchase successful!");
                console.log("Purchase Summary:", data);
            })
            .catch(error => alert("Error making purchase: " + error.message));
    }
    
    function sellStocks() {
        const stocksSelected = document.getElementById('stocks').selectedOptions;
        const quantity = document.getElementById('quantity').value;
    
        if (stocksSelected.length > 10) {
            alert("You can select up to 10 stocks.");
            return;
        }
    
        if (quantity < 1 || quantity > 10) {
            alert("Quantity must be between 1 and 10.");
            return;
        }
    
        // Logic for selling stocks
        let sellSummary = "Sold Stocks: ";
        for (let i = 0; i < stocksSelected.length; i++) {
            sellSummary += stocksSelected[i].value + " (Qty: " + quantity + "), ";
        }
        document.getElementById("purchase-summary").innerText = sellSummary;
    
        // Make the API call to process the sale
        const stocks = Array.from(stocksSelected).map(stock => stock.value);
        makePurchase([], stocks)
            .then(data => {
                alert("Sale successful!");
                console.log("Sale Summary:", data);
            })
            .catch(error => alert("Error making sale: " + error.message));
    }
    
    function buyCrypto() {
        const cryptosSelected = document.getElementById('cryptos').selectedOptions;
        const quantity = document.getElementById('crypto-quantity').value;
    
        if (cryptosSelected.length > 3) {
            alert("You can select up to 3 cryptos.");
            return;
        }
    
        if (quantity < 0.01 || quantity > 3) {
            alert("Quantity must be between 0.01 and 3.");
            return;
        }
    
        // Logic for purchasing cryptos
        let purchaseSummary = "Purchased Cryptos: ";
        for (let i = 0; i < cryptosSelected.length; i++) {
            purchaseSummary += cryptosSelected[i].value + " (Qty: " + quantity + "), ";
        }
        document.getElementById("purchase-summary").innerText = purchaseSummary;
    
        // Make the API call to process the purchase
        const cryptos = Array.from(cryptosSelected).map(crypto => crypto.value);
        makePurchase([], cryptos)
            .then(data => {
                alert("Purchase successful!");
                console.log("Purchase Summary:", data);
            })
            .catch(error => alert("Error making purchase: " + error.message));
    }
    
    function sellCrypto() {
        const cryptosSelected = document.getElementById('cryptos').selectedOptions;
        const quantity = document.getElementById('crypto-quantity').value;
    
        if (cryptosSelected.length > 3) {
            alert("You can select up to 3 cryptos.");
            return;
        }
    
        if (quantity < 0.01 || quantity > 3) {
            alert("Quantity must be between 0.01 and 3.");
            return;
        }
    
        // Logic for selling cryptos
        let sellSummary = "Sold Cryptos: ";
        for (let i = 0; i < cryptosSelected.length; i++) {
            sellSummary += cryptosSelected[i].value + " (Qty: " + quantity + "), ";
        }
        document.getElementById("purchase-summary").innerText = sellSummary;
    
        // Make the API call to process the sale
        const cryptos = Array.from(cryptosSelected).map(crypto => crypto.value);
        makePurchase([], cryptos)
            .then(data => {
                alert("Sale successful!");
                console.log("Sale Summary:", data);
            })
            .catch(error => alert("Error making sale: " + error.message));
    }

    document.getElementById("buy-stocks").addEventListener("click", buyStocks);
    document.getElementById("sell-stocks").addEventListener("click", sellStocks);
    document.getElementById("buy-cryptos").addEventListener("click", buyCrypto);
    document.getElementById("sell-cryptos").addEventListener("click", sellCrypto);

});


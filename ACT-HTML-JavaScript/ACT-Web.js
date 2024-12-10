// Base API URL
// const BASE_URL = "http://127.0.0.1:8000/api";

const BASE_URL = "http://127.0.0.1:8000/";
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
    purchaseForm.addEventListener("submit", function (e) {
        e.preventDefault();
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
    }
});

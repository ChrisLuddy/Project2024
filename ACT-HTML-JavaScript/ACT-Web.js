// Base API URL
// const BASE_URL = "http://161.35.38.50:8000/api";

const BASE_URL = "http://161.35.38.50:8000/api";
let accessToken = ""; // Store JWT token after login
// Retrieve token on page load
const storedToken = localStorage.getItem('accessToken');
if (storedToken) {
    accessToken = storedToken;
}

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
function handleLogin(email, password) {
    return fetch(`${BASE_URL}/token/`, {
        method: "POST",
        headers: getHeaders(false),
        body: JSON.stringify({ email, password }),
    })
    .then(response => {
        if (!response.ok) throw new Error("Invalid login credentials");
        return response.json();
    })
    .then(data => {
        accessToken = data.access;
        localStorage.setItem('accessToken', data.access);
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
// googleInit() {
   // google.accounts.id.initialize({
     //   client_id: 'GOOGLE_CLIENT_ID',
      //  callback: onGoogleSignIn,
  //  });

   // google.accounts.id.renderButton(
        //document.getElementById("google-login-btn"),
       // {
          //  theme: "outline",
          //  size: "large",
          //  shape: "pill"
       // }
   // );
//}

//.addEventListener("DOMContentLoaded", function () {
   // googleInit();
//});



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
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to fetch user details: ${response.status}`);
        }
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
    const loginForm = document.querySelector("#login-form");
    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        handleLogin(email, password)
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



// Fetch AI Prediction for selected asset
async function getAIPrediction(assetSymbol) {
    console.log('Fetching AI prediction for:', assetSymbol); // Debugging line
    try {
        const requestBody = JSON.stringify({ symbol: assetSymbol });
        console.log('Request Body:', requestBody); // Log request body

        const response = await fetch(`${BASE_URL}/act-ai/predict/`, {
            method: 'POST',
            headers: getHeaders(),
            body: requestBody
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log('API response data:', data); // Log the full response data for inspection

        if (data.forecast) { // Check if forecast exists in the response
            displayAIPrediction(data);
        } else {
            throw new Error('No AI predictions available.');
        }
    } catch (error) {
        console.error('Failed to fetch AI predictions:', error);
        alert('Failed to fetch AI predictions. Please try again.');
    }
}

// Display AI Prediction in the DOM
function displayAIPrediction(aiPrediction) {
    const resultDiv = document.getElementById('ai-prediction-result');
    console.log('AI Prediction:', aiPrediction); // Debugging line

    if (!aiPrediction) {
        resultDiv.textContent = 'No AI prediction available for the selected asset.';
        return;
    }

    const forecast = aiPrediction.forecast;
    resultDiv.innerHTML = `
        <strong>AI Prediction:</strong><br>
        Forecast: ${forecast}<br>
        Generated By User ID: ${aiPrediction.user_id}
    `;
}

// Function to initialize the AI Predictions page
document.addEventListener('DOMContentLoaded', function () {
    if (window.location.pathname.includes("ACT-AI-Predictions.html")) {
        const aiPredictionsContainer = document.querySelector('.ai-predictions-container');
        const stockSelect = document.createElement('select');
        const predictButton = document.createElement('button');
        const resultDiv = document.createElement('div');

        stockSelect.id = 'stock-select';
        stockSelect.className = 'stock-select';
        resultDiv.id = 'ai-prediction-result';
        ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'META', 'NVDA', 'AMD', 'INTC', 'NFLX', 'SPOT', 'ORCL', 'CSCO', 'BTC', 'ETH', 'XRP'].forEach(stock => {
            const option = document.createElement('option');
            option.value = stock;
            option.textContent = stock;
            stockSelect.appendChild(option);
        });

        predictButton.textContent = 'Get Prediction';
        predictButton.className = 'predict-button';
        predictButton.onclick = () => {
            const selectedStock = stockSelect.value;

            if (!accessToken) {
                resultDiv.innerHTML = '<div class="error-message">Please log in to view predictions.</div>';
                return;
            }

            getAIPrediction(selectedStock);
        };

        aiPredictionsContainer.appendChild(stockSelect);
        aiPredictionsContainer.appendChild(predictButton);
        aiPredictionsContainer.appendChild(resultDiv);
    }
});








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

// Function to get the access token from localStorage
function getAccessToken() {
    const token = localStorage.getItem('accessToken');
    if (token) {
        return token;
    }
    return null;
}

// Function to parse JWT token and extract the payload
function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

// Function to get the user_id from the access token
function getUserIdFromToken() {
    const accessToken = getAccessToken();
    if (accessToken) {
        const payload = parseJwt(accessToken);
        return payload.user_id;
    }
    return null;
}

// Function to refresh the access token
async function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        console.log("No refresh token found.");
        return null;
    }
}

// Function to get headers for API requests
function getHeaders(authRequired = true) {
    const headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    };
    const accessToken = getAccessToken();
    if (authRequired && accessToken) {
        headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return headers;
}

// Fetch fund manager details
async function fetchFundManagerDetails() {
    const token = getAccessToken();
    if (!token) return null;

    const response = await fetch(`${BASE_URL}/funds/`, {
        headers: getHeaders(true),
    });

    if (!response.ok) throw new Error("Unable to fetch fund manager details.");
    return response.json();
}

// Fetch clients associated with the fund manager
async function fetchClients() {
    const token = getAccessToken();
    if (!token) return [];

    const response = await fetch(`${BASE_URL}/clients/`, {
        headers: getHeaders(true),
    });

    if (!response.ok) throw new Error("Unable to fetch clients.");
    return response.json();
}

// Display the data on the Fund Manager's page
async function displayFundManagerPage() {
    try {
        const fundManagerDetails = await fetchFundManagerDetails();
        const fundManagerId = fundManagerDetails[0]?.user_id; 

        const clients = await fetchClients();
        const filteredClients = clients.filter(client => client.fund_manager_id === fundManagerId);

        const clientList = document.getElementById("client-list");
        clientList.innerHTML = ""; 

        filteredClients.forEach(client => {
            const clientItem = document.createElement("li");
            clientItem.textContent = client.name;
            clientList.appendChild(clientItem);
        });

        if (filteredClients.length === 0) {
            clientList.innerHTML = '<li>No clients available</li>';
        }

    } catch (error) {
        console.error("Error loading fund manager data:", error);
        alert("Error loading data. Please try again.");
    }
}

// Search function for clients, stocks, and cryptos
function searchData() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const clients = document.getElementById('client-list').querySelectorAll('li');
    const stocks = document.getElementById('stock-list').querySelectorAll('li');
    const cryptos = document.getElementById('crypto-list').querySelectorAll('li');

    // Filter clients
    clients.forEach(client => {
        const clientName = client.textContent.toLowerCase();
        client.style.display = clientName.includes(searchTerm) ? '' : 'none';
    });

    // Filter stocks
    stocks.forEach(stock => {
        const stockName = stock.textContent.toLowerCase();
        stock.style.display = stockName.includes(searchTerm) ? '' : 'none';
    });

    // Filter cryptos
    cryptos.forEach(crypto => {
        const cryptoName = crypto.textContent.toLowerCase();
        crypto.style.display = cryptoName.includes(searchTerm) ? '' : 'none';
    });
}

// Initialize the fund manager page
function initFundManagerPage() {
    const path = window.location.pathname;

    if (path.includes("ACT-Fund-Manager.html")) {
        const token = getAccessToken();
        if (!token) {
            alert("You need to be logged in to access the fund manager dashboard.");
            window.location.href = "ACT-Login.html"; // Redirect to login page if token is not available
            return;
        }

        // Display the fund manager dashboard data
        displayFundManagerPage();
    }
}

// Ensure the script runs once the page is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    initFundManagerPage(); // Initialize the fund manager page
});

// Function to get the access token from localStorage
function getAccessToken() {
    const token = localStorage.getItem('accessToken');
    if (token) {
        console.log("Access token retrieved: ", token);
        return token;
    }
    console.log("No access token found.");
    return null;
}

// Function to get the headers for the fetch request
function getHeaders(includeAuth = false) {
    const headers = {
        "Content-Type": "application/json",
    };
    if (includeAuth) {
        const token = getAccessToken();
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }
    }
    console.log("Request headers:", headers);
    return headers;
}

// Function to fetch the portfolio data for a logged-in fund administrator
function getPortfolioData() {
    const token = getAccessToken();
    if (!token) {
        alert("You need to be logged in to view the portfolio.");
        window.location.href = "ACT-Login.html";  // Redirect to login page
        return;
    }

    console.log("Fetching portfolio data with token:", token);

    fetch(`${BASE_URL}/portfolios/`, {
        method: "GET",
        headers: getHeaders(true)
    })
    .then(response => {
        console.log("Response received:", response);
        if (!response.ok) {
            throw new Error("Failed to fetch portfolio data. Status: " + response.status);
        }
        return response.json();
    })
    .then(data => {
        console.log("Portfolio data received:", data);
        if (data && data.length > 0) {
            fetchAssets(data);
        } else {
            console.error("No portfolios found for the logged-in fund administrator.");
            alert("No portfolios found for your account.");
        }
    })
    .catch(error => {
        console.error("Error fetching portfolio data:", error);
        alert("An error occurred while fetching portfolio data.");
    });
}

// Function to fetch assets and associate them with portfolios
function fetchAssets(portfolios) {
    const token = getAccessToken();
    if (!token) {
        alert("You need to be logged in to view the portfolio.");
        window.location.href = "ACT-Login.html";  // Redirect to login page
        return;
    }

    console.log("Fetching assets with token:", token);

    fetch(`${BASE_URL}/assets/`, {
        method: "GET",
        headers: getHeaders(true)
    })
    .then(response => {
        console.log("Assets response received:", response);
        if (!response.ok) {
            console.error("Failed to fetch assets data. Status:", response.status, response.statusText);
            throw new Error("Failed to fetch assets data. Status: " + response.status);
        }
        return response.json();
    })
    .then(data => {
        console.log("Assets data received:", data);
        const assetsByPortfolio = data.reduce((acc, asset) => {
            acc[asset.portfolio_id] = acc[asset.portfolio_id] || [];
            acc[asset.portfolio_id].push(asset);
            return acc;
        }, {});

        portfolios.forEach(portfolio => {
            portfolio.assets = assetsByPortfolio[portfolio.fund_id] || [];
        });

        displayPortfolioData(portfolios);
    })
    .catch(error => {
        console.error("Error fetching assets data:", error);
        alert("An error occurred while fetching assets data.");
    });
}

// Function to display the fetched portfolio data under the correct categories (Tech Stocks & Cryptos)
function displayPortfolioData(portfolios) {
    const stockList = document.getElementById("stock-list");
    const cryptoList = document.getElementById("crypto-list");

    if (!stockList || !cryptoList) {
        console.error("Stock or crypto list element not found in the DOM.");
        return;
    }

    // Clear existing lists
    stockList.innerHTML = "";
    cryptoList.innerHTML = "";

    const assets = [];
    portfolios.forEach(portfolio => {
        if (portfolio.name === "Tech Stocks Portfolio" || portfolio.name === "Crypto Portfolio") {
            assets.push(...portfolio.assets);
        }
    });

    if (assets.length === 0) {
        console.log("No assets to display.");
    }

    // Define asset categories for classification
    const cryptoAssets = ['BTC', 'ETH', 'XRP', 'USDT', 'BNB', 'ADA', 'SOL', 'DOT', 'DOGE', 'AVAX'];

    // Loop through the asset data and classify assets into stocks or cryptos
    assets.forEach(asset => {
        const listItem = document.createElement("li");
        listItem.textContent = `${asset.symbol} - ${asset.quantity}`;

        if (cryptoAssets.includes(asset.symbol)) {
            // If asset is a cryptocurrency
            cryptoList.appendChild(listItem);
        } else {
            // Otherwise, it is a tech stock
            stockList.appendChild(listItem);
        }
    });
}

// Initialize the portfolio page 
function initPortfolioPage() {
    const path = window.location.pathname;
    if (path.includes("ACT-Portfolio.html")) {
        const token = getAccessToken();
        if (!token) {
            alert("You need to be logged in to view the portfolio.");
            window.location.href = "ACT-Login.html";  // Redirect to login page if token is not available
            return;
        }

        // Fetch portfolio data if token exists
        getPortfolioData();
    }
}

// Ensure the script runs once the page is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    initPortfolioPage(); // Initialize the portfolio page
});

// Define stocks and cryptocurrencies
const stocks = {
    'AAPL': 'Apple',
    'GOOG': 'Google',
    'MSFT': 'Microsoft',
    'AMZN': 'Amazon',
    'TSLA': 'Tesla',
    'META': 'Meta',
    'NVDA': 'NVIDIA',
    'AMD': 'AMD',
    'INTC': 'Intel',
    'NFLX': 'Netflix',
    'SPOT': 'Spotify',
    'ORCL': 'Oracle',
    'CSCO': 'Cisco'
};

const cryptos = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'XRP': 'Ripple',
};

// Fetch available assets
async function fetchAssets() {
    console.log("Fetching assets...");
    const token = getAccessToken();
    if (!token) {
        console.log("No token found, redirecting to login.");
        alert("You need to be logged in to proceed.");
        window.location.href = "ACT-Login.html";
        return [];
    }

    try {
        const response = await fetch(`${BASE_URL}/assets/`, {
            headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        });

        if (!response.ok) throw new Error("Failed to fetch assets.");
        const backendAssets = await response.json();
        console.log("Assets fetched from backend:", backendAssets);
        return [...backendAssets, ...formatPredefinedAssets()];
    } catch (error) {
        console.error("Error fetching assets:", error);
        return [];
    }
}

// Format predefined assets into a common structure
function formatPredefinedAssets() {
    console.log("Formatting predefined assets...");
    const formattedStocks = Object.keys(stocks).map(symbol => ({
        id: symbol,
        symbol: symbol,
        name: stocks[symbol],
        type: 'stock'
    }));

    const formattedCryptos = Object.keys(cryptos).map(symbol => ({
        id: symbol,
        symbol: symbol,
        name: cryptos[symbol],
        type: 'crypto'
    }));

    console.log("Formatted stocks:", formattedStocks);
    console.log("Formatted cryptos:", formattedCryptos);

    return [...formattedStocks, ...formattedCryptos];
}

// Populate dropdowns dynamically
async function populateDropdowns() {
    console.log("Populating dropdowns...");
    try {
        const assets = await fetchAssets();

        const stockDropdown = document.getElementById("stocks");
        const cryptoDropdown = document.getElementById("cryptos");

        if (!stockDropdown || !cryptoDropdown) {
            console.error("Dropdown elements not found.");
            return;
        }

        stockDropdown.innerHTML = "";
        cryptoDropdown.innerHTML = "";

        // Populate predefined stocks
        Object.keys(stocks).forEach(symbol => {
            const option = document.createElement("option");
            option.value = symbol;
            option.textContent = `${symbol} (${stocks[symbol]})`;
            stockDropdown.appendChild(option);
        });

        // Populate predefined cryptos
        Object.keys(cryptos).forEach(symbol => {
            const option = document.createElement("option");
            option.value = symbol;
            option.textContent = `${symbol} (${cryptos[symbol]})`;
            cryptoDropdown.appendChild(option);
        });

        // Append assets from backend
        assets.forEach(asset => {
            const option = document.createElement("option");
            option.value = asset.id;
            option.textContent = `${asset.symbol} (${asset.name})`;
            if (asset.type === "stock") {
                stockDropdown.appendChild(option);
            } else if (asset.type === "crypto") {
                cryptoDropdown.appendChild(option);
            }
        });
        console.log("Dropdowns populated successfully.");
    } catch (error) {
        console.error("Error populating dropdowns:", error);
    }
}

// Create a new order (buy/sell)
async function createOrder(orderType, assetId, quantity) {
    console.log(`Creating order: type=${orderType}, assetId=${assetId}, quantity=${quantity}`);
    const token = getAccessToken();
    if (!token) {
        console.log("No token found, redirecting to login.");
        alert("You need to be logged in to proceed.");
        window.location.href = "ACT-Login.html";
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/orders/`, {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                type: orderType,
                asset_id: assetId,
                quantity: quantity,
            }),
        });

        if (!response.ok) throw new Error("Failed to create order.");
        const orderResponse = await response.json();
        console.log("Order created successfully:", orderResponse);
        return orderResponse;
    } catch (error) {
        console.error("Error creating order:", error);
        throw error;
    }
}

// Handle buy/sell logic for both stocks and cryptos
async function handleTransaction(orderType, isCrypto) {
    console.log(`Handling transaction: orderType=${orderType}, isCrypto=${isCrypto}`);
    try {
        const dropdown = document.getElementById(isCrypto ? "cryptos" : "stocks");
        const quantityInput = document.getElementById(isCrypto ? "crypto-quantity" : "stock-quantity");

        if (!dropdown || !quantityInput) {
            console.error("Dropdown or quantity input not found.");
            return;
        }

        const selectedOption = dropdown.options[dropdown.selectedIndex];
        const quantity = parseFloat(quantityInput.value);

        if (!selectedOption || quantity <= 0) {
            console.error("Invalid asset or quantity.");
            alert("Please select a valid asset and quantity.");
            return;
        }

        const assetId = selectedOption.value;
        console.log(`Selected asset: ${selectedOption.text}, quantity: ${quantity}`);

        // Create the order (buy/sell)
        await createOrder(orderType, assetId, quantity);
        alert(`${orderType === "buy" ? "Purchase" : "Sale"} successful for ${selectedOption.text}.`);
        console.log(`${orderType} successful for ${selectedOption.text}`);
        populateDropdowns();
    } catch (error) {
        console.error("Error processing transaction:", error);
        alert("An error occurred during the transaction.");
    }
}

// Attach event listeners
document.addEventListener("DOMContentLoaded", async () => {
    console.log("Document loaded, initializing...");
    if (window.location.pathname.includes("ACT-Purchase.html")) {
        await populateDropdowns();

        const buyStocksButton = document.getElementById("buy-stocks");
        const sellStocksButton = document.getElementById("sell-stocks");
        const buyCryptosButton = document.getElementById("buy-cryptos");
        const sellCryptosButton = document.getElementById("sell-cryptos");

        if (buyStocksButton) {
            buyStocksButton.addEventListener("click", () => {
                console.log("Buy stocks button clicked.");
                handleTransaction("buy", false);
            });
        }
        if (sellStocksButton) {
            sellStocksButton.addEventListener("click", () => {
                console.log("Sell stocks button clicked.");
                handleTransaction("sell", false);
            });
        }
        if (buyCryptosButton) {
            buyCryptosButton.addEventListener("click", () => {
                console.log("Buy cryptos button clicked.");
                handleTransaction("buy", true);
            });
        }
        if (sellCryptosButton) {
            sellCryptosButton.addEventListener("click", () => {
                console.log("Sell cryptos button clicked.");
                handleTransaction("sell", true);
            });
        }
        console.log("Event listeners attached.");
    }
});



const assets = {
    'AAPL': 'Apple',
    'GOOG': 'Google',
    'MSFT': 'Microsoft',
    'AMZN': 'Amazon',
    'TSLA': 'Tesla',
    'META': 'Meta',
    'NVDA': 'NVIDIA',
    'AMD': 'AMD',
    'INTC': 'Intel',
    'NFLX': 'Netflix',
    'SPOT': 'Spotify',
    'ORCL': 'Oracle',
    'CSCO': 'Cisco',
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'XRP': 'Ripple'
};

// Function to get the access token from localStorage
function getAccessToken() {
    const token = localStorage.getItem('accessToken');
    if (token) {
        console.log("Access token retrieved: ", token);
        return token;
    }
    console.log("No access token found.");
    return null;
}

// Function to parse JWT token and extract the payload
function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

// Function to get the user_id from the access token
function getUserIdFromToken() {
    if (accessToken) {
        const payload = parseJwt(accessToken);
        return payload.user_id;
    }
    return null;
}

// Function to refresh the access token
async function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        console.log("No refresh token found.");
        return null;
    }
}

// Fetch Trade Rating for selected asset
async function getTradeRating(assetSymbol) {
    console.log('Fetching trade rating for:', assetSymbol); // Debugging line
    try {
        const response = await fetch(`${BASE_URL}/act-ai/trade-rating/?symbol=${assetSymbol}`, {
            method: 'GET',
            headers: getHeaders()
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        const tradeRating = data.trade_rating;
        displayTradeRating(tradeRating);
    } catch (error) {
        console.error('Failed to fetch trade ratings:', error);
        alert('Failed to fetch trade ratings. Please try again.');
    }
}

// Display Trade Rating in the DOM
function displayTradeRating(tradeRating) {
    const ratingTextElement = document.getElementById('trade-rating-text');
    console.log('Trade Rating:', tradeRating); // Debugging line

    if (!tradeRating) {
        ratingTextElement.textContent = 'No trade rating available for the selected asset.';
        return;
    }

    const rating = tradeRating.rating;
    ratingTextElement.innerHTML = `
        <strong>Trade Rating for ${tradeRating.symbol}:</strong><br>
        Rating: ${rating}<br>
        Last Updated: ${new Date(tradeRating.timestamp).toLocaleString()}
    `;
}

// Function to initialize the trade ratings page
function initTradeRatingsPage() {
    // Event Listener for the 'Get Trade Rating' button
    document.getElementById('get-stock-rating').addEventListener('click', () => {
        console.log('Button clicked!'); // Debugging line
        const stockSelect = document.getElementById('stock-select');
        const selectedStock = stockSelect.value;
        console.log('Selected Stock:', selectedStock); // Debugging line
        getTradeRating(selectedStock);
    });

    // Event Listener for the 'Get Crypto Rating' button
    document.getElementById('get-crypto-rating').addEventListener('click', () => {
        console.log('Button clicked!'); // Debugging line
        const cryptoSelect = document.getElementById('crypto-select');
        const selectedCrypto = cryptoSelect.value;
        console.log('Selected Crypto:', selectedCrypto); // Debugging line
        getTradeRating(selectedCrypto);
    });
}

// Function to get the access token from localStorage
function getAccessToken() {
    const token = localStorage.getItem('accessToken');
    if (token) {
        console.log("Access token retrieved: ", token);
        return token;
    }
    console.log("No access token found.");
    return null;
}

// Function to parse JWT token and extract the payload
function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

// Function to get headers for API requests
function getHeaders(authRequired = true) {
    const headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    };
    const accessToken = getAccessToken();
    if (authRequired && accessToken) {
        headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return headers;
}

// Function to refresh the access token
async function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        console.log("No refresh token found.");
        return null;
    }
    
}

function initOrderSystem() {
    const buyStocksButton = document.getElementById('buy-stocks');
    const sellStocksButton = document.getElementById('sell-stocks');
    const buyCryptosButton = document.getElementById('buy-cryptos');
    const sellCryptosButton = document.getElementById('sell-cryptos');

    // Function to handle order submission
    function handleOrderSubmission(event, assetType, orderType) {
        event.preventDefault();

        let selectedAsset, quantity, portfolioId;

        if (assetType === 'stock') {
            selectedAsset = document.getElementById('stocks').value;
            quantity = document.getElementById('stock-quantity').value;
            portfolioId = 1; 
        } else if (assetType === 'crypto') {
            selectedAsset = document.getElementById('cryptos').value;
            quantity = document.getElementById('crypto-quantity').value;
            portfolioId = 2; 
        }

        if (!selectedAsset || !quantity) {
            console.error('Asset and quantity must be selected.');
            return;
        }

        const order = {
            amount: parseFloat(quantity),
            order_type: orderType,
            portfolio_id: portfolioId
        };

        fetch(`${BASE_URL}/orders/`, {
            method: 'POST',
            headers: getHeaders(true),
            body: JSON.stringify(order)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Order submitted:', data);
            // Handle successful order submission
        })
        .catch(error => {
            console.error('Error submitting order:', error);
            // Handle order submission error 
        });
    }

    // Event listeners for buy and sell buttons
    buyStocksButton.addEventListener('click', function (event) {
        handleOrderSubmission(event, 'stock', 'buy');
    });

    sellStocksButton.addEventListener('click', function (event) {
        handleOrderSubmission(event, 'stock', 'sell');
    });

    buyCryptosButton.addEventListener('click', function (event) {
        handleOrderSubmission(event, 'crypto', 'buy');
    });

    sellCryptosButton.addEventListener('click', function (event) {
        handleOrderSubmission(event, 'crypto', 'sell');
    });
}

document.addEventListener('DOMContentLoaded', initOrderSystem);




// Function to get the access token from localStorage
function getAccessToken() {
    const token = localStorage.getItem('accessToken');
    if (token) {
        console.log("Access token retrieved: ", token);
        return token;
    }
    console.log("No access token found.");
    return null;
}

// Function to parse JWT token and extract the payload
function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

// Function to refresh the access token
async function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        console.log("No refresh token found.");
        return null;
    }

    const response = await fetch(`${BASE_URL}/token/refresh/`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ refresh: refreshToken })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('accessToken', data.access);
        return data.access;
    } else {
        console.error("Failed to refresh access token.");
        return null;
    }
}

// Helper function to set headers
function getHeaders(authRequired = true) {
    const headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    };
    const token = getAccessToken();
    if (authRequired && token) {
        headers["Authorization"] = `Bearer ${token}`;
    }
    console.log("Request headers:", headers);
    return headers;
}

// Fetch all assets for the fund administrator using the access token
async function fetchAllAssets() {
    const response = await fetch(`${BASE_URL}/assets/`, { headers: getHeaders(true) });
    if (!response.ok) {
        if (response.status === 401) {
            console.log("Token expired. Refreshing token...");
            const newToken = await refreshAccessToken();
            if (newToken) {
                return fetchAllAssets(); // Retry the request with the new token
            } else {
                throw new Error("Failed to refresh token and fetch assets.");
            }
        }
        throw new Error(`Failed to fetch assets: ${response.status} ${response.statusText}`);
    }
    return response.json();
}

// Populate stocks and cryptos in the HTML
async function populateReports() {
    try {
        const token = getAccessToken();
        const parsedToken = parseJwt(token);

        const assets = await fetchAllAssets();

        const stockList = document.getElementById("stock-list");
        const cryptoList = document.getElementById("crypto-list");

        const assetSymbols = {
            'AAPL': 'Apple',
            'GOOG': 'Google',
            'MSFT': 'Microsoft',
            'AMZN': 'Amazon',
            'TSLA': 'Tesla',
            'META': 'Meta',
            'NVDA': 'NVIDIA',
            'AMD': 'AMD',
            'INTC': 'Intel',
            'NFLX': 'Netflix',
            'SPOT': 'Spotify',
            'ORCL': 'Oracle',
            'CSCO': 'Cisco',
            'BTC': 'Bitcoin',
            'ETH': 'Ethereum',
            'XRP': 'Ripple'
        };

        assets.forEach(asset => {
            const li = document.createElement("li");
            li.textContent = `${asset.symbol} (${assetSymbols[asset.symbol] || 'Unknown'}) - ${asset.amount}`;
            if (["BTC", "ETH", "XRP"].includes(asset.symbol)) { 
                cryptoList.appendChild(li);
            } else {
                stockList.appendChild(li);
            }
        });
    } catch (error) {
        console.error("Error populating reports:", error);
    }
}

// Initialize Report Page
async function initReportPage() {
    const token = getAccessToken();
    if (!token) {
        alert("You need to be logged in to view the reports.");
        return;
    }

    try {
        // Attempt to retrieve assets to verify authentication
        await populateReports();
    } catch (error) {
        console.error("Error initializing report page:", error);
        alert("Unable to authenticate. Please log in again.");
    }

    document.getElementById('download-pdf').addEventListener('click', () => {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        doc.text("Financial Reports", 10, 10);
        doc.text("Stocks", 10, 20);
        document.querySelectorAll("#stock-list li").forEach((li, index) => {
            doc.text(`${index + 1}. ${li.textContent}`, 10, 30 + index * 10);
        });

        doc.text("Cryptocurrencies", 10, 40 + document.querySelectorAll("#stock-list li").length * 10);
        document.querySelectorAll("#crypto-list li").forEach((li, index) => {
            doc.text(`${index + 1}. ${li.textContent}`, 10, 50 + document.querySelectorAll("#stock-list li").length * 10 + index * 10);
        });

        doc.save("financial-report.pdf");
    });

    document.getElementById('download-csv').addEventListener('click', () => {
        let csvContent = "data:text/csv;charset=utf-8,Type,Symbol,Amount\n";
        document.querySelectorAll("#stock-list li").forEach(li => {
            csvContent += `Stock,${li.textContent.split(' - ')[0]},${li.textContent.split(' - ')[1]}\n`;
        });
        document.querySelectorAll("#crypto-list li").forEach(li => {
            csvContent += `Crypto,${li.textContent.split(' - ')[0]},${li.textContent.split(' - ')[1]}\n`;
        });

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "financial-report.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
}

// Call the initialization function when the page loads
document.addEventListener('DOMContentLoaded', initReportPage);







// Helper function to set headers
function getHeaders(authRequired = true) {
    const headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    };
    const accessToken = getAccessToken();
    if (authRequired && accessToken) {
        headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return headers;
}

// Function to get the access token from localStorage
function getAccessToken() {
    const token = localStorage.getItem('accessToken');
    if (token) {
        console.log("Access token retrieved: ", token);
        return token;
    }
    console.log("No access token found.");
    return null;
}

// Function to parse JWT token and extract the payload
function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

// Function to refresh the access token
async function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        console.log("No refresh token found.");
        return null;
    }
    
}

// Function to get the user_id from the access token
function getUserIdFromToken() {
    const accessToken = getAccessToken();
    if (accessToken) {
        const payload = parseJwt(accessToken);
        return payload.user_id;
    }
    return null;
}

// Fetch fund manager details
async function fetchFundManagerDetails() {
    const token = getAccessToken();
    if (!token) return null;

    const response = await fetch(`${BASE_URL}/funds/`, {
        headers: getHeaders(true),
    });

    if (!response.ok) throw new Error("Unable to fetch fund manager details.");
    const data = await response.json();
    console.log("Fund manager details:", data);
    return data;
}

// Fetch clients associated with the fund manager
async function fetchClients() {
    const token = getAccessToken();
    if (!token) return [];

    const response = await fetch(`${BASE_URL}/clients/`, {
        headers: getHeaders(true),
    });

    if (!response.ok) throw new Error("Unable to fetch clients.");
    const data = await response.json();
    console.log("Clients data:", data);
    return data;
}

// Display the data on the Fund Manager's page
async function displayFundManagerPage() {
    try {
        const fundManagerId = getUserIdFromToken();
        console.log("Fund Manager ID:", fundManagerId);

        const clients = await fetchClients();
        const filteredClients = clients.filter(client => client.fund_manager_id === fundManagerId);

        const clientList = document.getElementById("client-list");
        clientList.innerHTML = ""; // Clear the list

        filteredClients.forEach(client => {
            const clientItem = document.createElement("li");
            clientItem.textContent = `Client: ${client.name}`;
            clientList.appendChild(clientItem);
        });

        if (filteredClients.length === 0) {
            clientList.innerHTML = '<li>No clients available</li>';
        }

    } catch (error) {
        console.error("Error loading fund manager data:", error);
        alert("Error loading data. Please try again.");
    }
}

// Search function for clients, stocks, and cryptos
function searchData() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const clients = document.getElementById('client-list').querySelectorAll('li');
    const stocks = document.getElementById('stock-list').querySelectorAll('li');
    const cryptos = document.getElementById('crypto-list').querySelectorAll('li');

    // Filter clients
    clients.forEach(client => {
        const clientName = client.textContent.toLowerCase();
        client.style.display = clientName.includes(searchTerm) ? '' : 'none';
    });

    // Filter stocks
    stocks.forEach(stock => {
        const stockName = stock.textContent.toLowerCase();
        stock.style.display = stockName.includes(searchTerm) ? '' : 'none';
    });

    // Filter cryptos
    cryptos.forEach(crypto => {
        const cryptoName = crypto.textContent.toLowerCase();
        crypto.style.display = cryptoName.includes(searchTerm) ? '' : 'none';
    });
}

// Initialize the fund manager page
function initFundManagerPage() {
    const path = window.location.pathname;

    if (path.includes("ACT-Fund-Manager.html")) {
        const token = getAccessToken();
        if (!token) {
            alert("You need to be logged in to access the fund manager dashboard.");
            window.location.href = "ACT-Login.html"; // Redirect to login page if token is not available
            return;
        }

        // Display the fund manager dashboard data
        displayFundManagerPage();
    }
}

// Ensure the script runs once the page is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    initFundManagerPage(); // Initialize the fund manager page
});


// Function to get chat response from the AI API
async function getChatbotResponse(message) {
    const user_id = getUserIdFromToken();
    if (!user_id) {
        return "User ID not found. Please log in again.";
    }

    const url = `${BASE_URL}/act-ai/chat/`;
    const payload = {
        message: message,
        user_id: user_id
    };

    try {
        console.log("Sending request to AI API with payload:", payload);
        const response = await fetch(url, {
            method: "POST",
            headers: getHeaders(),
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }

        const data = await response.json();
        console.log("Received response from AI API:", data);
        return data.reply || "I'm sorry, I couldn't process your request.";
    } catch (error) {
        console.error("Error fetching chatbot response:", error);
        return "There was an error processing your request. Please try again later.";
    }
}

// Function to initialize the chatbot page
function initChatbotPage() {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatLog = document.getElementById("chat-log");

    chatForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        const userMessage = userInput.value;
        addMessageToChatLog("user", userMessage);

        const response = await getChatbotResponse(userMessage);
        addMessageToChatLog("bot", response);

        userInput.value = ""; // Clear the input field
    });

    function addMessageToChatLog(sender, message) {
        const messageElement = document.createElement("div");
        messageElement.className = `chat-message ${sender}`;
        messageElement.textContent = message;
        chatLog.appendChild(messageElement);
        chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom
    }
}

// Function to get the access token from localStorage
function getAccessToken() {
    const token = localStorage.getItem('accessToken');
    if (token) {
        console.log("Access token retrieved: ", token);
        return token;
    }
    console.log("No access token found.");
    return null;
}

// Function to parse JWT token and extract the payload
function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

// Function to get the user_id from the access token
function getUserIdFromToken() {
    if (accessToken) {
        const payload = parseJwt(accessToken);
        return payload.user_id;
    }
    return null;
}

// Function to refresh the access token
async function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        console.log("No refresh token found.");
        return null;
    }
    
}

// Fetch and display support requests for the logged-in user
async function fetchSupportRequests() {
    try {
        const userId = getUserIdFromToken();
        const response = await fetch(`${BASE_URL}/support-requests/`, {
            method: 'GET',
            headers: getHeaders()
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        const userSupportRequests = data.filter(request => request.user_id === userId);
        displaySupportRequests(userSupportRequests);
    } catch (error) {
        console.error('Failed to fetch support requests:', error);
        alert('Failed to fetch support requests. Please try again.');
    }
}

// Display support requests in the DOM
function displaySupportRequests(supportRequests) {
    const reviewsContainer = document.getElementById('reviews-container');
    reviewsContainer.innerHTML = ''; // Clear existing content

    supportRequests.forEach(request => {
        const requestElement = document.createElement('div');
        requestElement.className = 'review-item';
        requestElement.innerHTML = `
            <p><strong>Request:</strong> ${request.request}</p>
        `;
        reviewsContainer.appendChild(requestElement);
    });
}

// Submit a new support request
async function submitSupportRequest(userId, requestContent) {
    try {
        const requestBody = JSON.stringify({ user_id: userId, request: requestContent });
        const response = await fetch(`${BASE_URL}/support-requests/`, {
            method: 'POST',
            headers: getHeaders(),
            body: requestBody
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log('Support request submitted:', data);
        fetchSupportRequests(); // Refresh the support requests list
    } catch (error) {
        console.error('Failed to submit support request:', error);
        alert('Failed to submit support request. Please try again.');
    }
}

// Initialize the reviews page
function initReviewsPage() {
    fetchSupportRequests(); // Fetch and display support requests

    // Event listener for submitting reviews
    document.getElementById('submit-review').addEventListener('click', () => {
        const reviewText = document.getElementById('review-text').value;
        const userId = getUserIdFromToken();

        if (!reviewText || !userId) {
            alert('Please provide a review and ensure you are logged in.');
            return;
        }

        submitSupportRequest(userId, reviewText);
    });
}

// Function to get the access token from localStorage
function getAccessToken() {
    const token = localStorage.getItem('accessToken');
    if (token) {
        console.log("Access token retrieved: ", token);
        return token;
    }
    console.log("No access token found.");
    return null;
}

// Function to parse JWT token and extract the payload
function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

// Function to get the user_id from the access token
function getUserIdFromToken() {
    if (accessToken) {
        const payload = parseJwt(accessToken);
        return payload.user_id;
    }
    return null;
}

// Function to refresh the access token
async function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        console.log("No refresh token found.");
        return null;
    }
    
}

const fetchAmount = async (symbol) => {
    const response = await fetch(`${BASE_URL}/assets/`, {
        headers: getHeaders(true)
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    const asset = data.find(asset => asset.symbol === symbol);

    if (!asset) {
        console.error(`Asset with symbol ${symbol} not found`);
        return null;
    }

    const amount = asset.amount;
    localStorage.setItem(`${symbol}_amount`, amount); // Save amount to localStorage
    return amount;
};

// Function to check price alerts
function checkPriceAlerts() {
    const alerts = JSON.parse(localStorage.getItem('priceAlerts')) || [];

    alerts.forEach(async (alert) => {
        try {
            const currentAmount = await fetchAmount(alert.asset);
            if (currentAmount !== null && // Ensure currentAmount is valid
                ((alert.thresholdType === 'above' && currentAmount > alert.priceThreshold) ||
                (alert.thresholdType === 'below' && currentAmount < alert.priceThreshold))) {
                showBrowserNotification(alert.asset, currentAmount, alert.thresholdType);
            }
        } catch (error) {
            console.error('Error checking price alerts:', error);
        }
    });
}

// Function to periodically check the amount every hour
function checkAmountPeriodically() {
    setInterval(() => {
        checkPriceAlerts(); // Call checkPriceAlerts function to update amounts and notifications
    }, 3600000); // Check every hour (3600000 ms)
}

// Call the function to start checking amounts periodically
checkAmountPeriodically();

// Define showBrowserNotification function before it is used
function showBrowserNotification(asset, amount, thresholdType) {
    if (Notification.permission === 'granted') {
        new Notification(`Price Alert: ${asset}`, {
            body: `The amount has ${thresholdType} ${amount}.`,
            icon: 'images/ACT-Logo.png'
        });
    } else if (Notification.permission !== 'denied') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                new Notification(`Price Alert: ${asset}`, {
                    body: `The amount has ${thresholdType} ${amount}.`,
                    icon: 'images/ACT-Logo.png'
                });
            }
        });
    }
}

// Function to initialize the price alert system for Fund Administrators
function initPriceAlertSystem() {
    const alertForm = document.getElementById('alert-form');
    const assetSelect = document.getElementById('asset');
    const alertMessages = document.getElementById('alert-messages');
    const clientAlerts = document.getElementById('client-alerts');
    const clientList = document.getElementById('client-list');
    const searchClientInput = document.getElementById('search-client');

    const assets = {
        'AAPL': 'Apple',
        'GOOG': 'Google',
        'MSFT': 'Microsoft',
        'AMZN': 'Amazon',
        'TSLA': 'Tesla',
        'META': 'Meta',
        'NVDA': 'NVIDIA',
        'AMD': 'AMD',
        'INTC': 'Intel',
        'NFLX': 'Netflix',
        'SPOT': 'Spotify',
        'ORCL': 'Oracle',
        'CSCO': 'Cisco',
        'BTC': 'Bitcoin',
        'ETH': 'Ethereum',
        'XRP': 'Ripple'
    };

    for (const [symbol, name] of Object.entries(assets)) {
        const option = document.createElement('option');
        option.value = symbol;
        option.text = `${symbol} (${name})`;
        assetSelect.appendChild(option);
    }

    alertForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const selectedAsset = assetSelect.value;
        const priceThreshold = document.getElementById('price-threshold').value;
        const thresholdType = document.querySelector('input[name="threshold-type"]:checked').value;

        const alert = {
            asset: selectedAsset,
            priceThreshold: priceThreshold,
            thresholdType: thresholdType
        };

        // Save the alert in local storage
        let alerts = JSON.parse(localStorage.getItem('priceAlerts')) || [];
        alerts.push(alert);
        localStorage.setItem('priceAlerts', JSON.stringify(alerts));
        
        alertMessages.textContent = 'Alert set successfully!';
        showBrowserNotification(selectedAsset, priceThreshold, thresholdType);
        
        // Call function to check price alerts periodically
        checkPriceAlerts();
    });

    function fetchClientAlerts() {
        fetch(`${BASE_URL}/assets/`, {
            headers: getHeaders(true)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(assetsData => {
            const alerts = JSON.parse(localStorage.getItem('priceAlerts')) || [];
            assetsData.forEach(asset => {
                const alert = alerts.find(a => a.asset === asset.symbol);
                if (alert) {
                    localStorage.setItem(`${asset.symbol}_amount`, asset.amount);
                    if ((alert.thresholdType === 'above' && asset.amount > alert.priceThreshold) ||
                        (alert.thresholdType === 'below' && asset.amount < alert.priceThreshold)) {
                        showBrowserNotification(asset.symbol, asset.amount, alert.thresholdType);
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching assets data:', error);
            alertMessages.textContent = 'Error fetching assets data. Please try again later.';
        });

        fetch(`${BASE_URL}/clients/`, {
            headers: getHeaders(true)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(clientsData => {
            clientAlerts.innerHTML = '';
            clientList.innerHTML = '';
            let hasPriceAlerts = false;
            const clientsSet = new Set();

            clientsData.forEach(client => {
                clientsSet.add(client.name);
                if (client.alerts && client.alerts.length > 0) {
                    hasPriceAlerts = true;
                    client.alerts.forEach(alert => {
                        clientAlerts.innerHTML += `Client: ${client.name}, Asset: ${alert.asset}, Price Threshold: ${alert.priceThreshold}, Type: ${alert.thresholdType}<br>`;
                    });
                }
            });

            if (!hasPriceAlerts) {
                clientAlerts.innerHTML = 'There are currently no clients with price alerts.<br>';
            }

            clientAlerts.innerHTML += '<h3>Clients</h3>';
            clientsSet.forEach(clientName => {
                clientAlerts.innerHTML += `Client: ${clientName}<br>`;
            });
        })
        .catch(error => {
            console.error('Error fetching clients data:', error);
            alertMessages.textContent = 'Error fetching clients data. Please try again later.';
        });
    }

    searchClientInput.addEventListener('input', function () {
        const searchTerm = searchClientInput.value.toLowerCase();
        const clients = clientList.querySelectorAll('li');
        clients.forEach(client => {
            const clientName = client.textContent.toLowerCase();
            client.style.display = clientName.includes(searchTerm) ? '' : 'none';
        });
    });

    fetchClientAlerts();
}

document.addEventListener('DOMContentLoaded', initPriceAlertSystem);

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
    } else if (window.location.pathname.includes("ACT-Fund-Manager-Welcome.html")) {
        updateFundManagerWelcome();
    } else if (path.includes("ACT-Price-System.html")) {
        initPriceAlertSystem();
    } else if (path.includes("ACT-Reports.html")) {
        initReportPage();
    } else if (path.includes("ACT-AI-Chatbot.html")) {
        initChatbotPage();
    } else if (path.includes("ACT-Reviews.html")) {
        initReviewsPage();
    } else if (path.includes("ACT-Trade-Ratings.html")) {
        initTradeRatingsPage();
    } else if (path.includes("ACT-Portfolio.html")) {
        initPortfolioPage();
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
});




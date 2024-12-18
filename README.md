# Project2024
ACT (Agentic Corporate Trader)
# Project Readme File


## Table of contents 
- [Features of the website](#features)
- [Database Configuration](#database-configuration)
- [Data Model Overview](#data-model-overview)
- [Database Diagram](#database-diagram)
- [Backend](#backend)
- [API](#api)
- [Frontend](#frontend)
- [css](#css)
- [Ai](#ai)
- [Docker Integration](#docker-integration)
- [Product Backlog](#product-backlog)

### Features
Features for the website:
1. User Authentication and Access Control
•	User Login/Logout
•	Role-based Access Control
•	Session Management
•	Forgot Password/Reset Password
2. Dashboard Overview
•	Client Overview (total clients, account statuses)
•	Market Overview (current stock/market prices/news Section)
•	Recent Activities Log
•	Graphical Analysis (performance graphs)
3. Client Management
•	Client Profiles (personal info, portfolio details)
•	Client Search and Filter
•	Client Communication (email or chat integration)
•	Client Segmentation (by risk profile, investment goals)
4. Portfolio Management
•	View and Manage Portfolios
•	Investment Strategy Settings
•	Trade Execution (buy/sell functionality)
•	Portfolio Performance Tracking
•	Asset Allocation Management
•	Risk Management Tools (risk exposure analysis)
5. Market and Price Alerts
•	Set Price/Performance Alerts
•	Real-time Alert Notifications
•	Watchlist Management
6. Trading and Transaction Management
•	Place Trades (stocks, crypto currencies)
•	Order History
•	Transaction Fees Tracking
•	Support for Different Order Types (market, limit, stop-loss)
•	Trade Execution Report
7. Reporting and Analytics
•	Generate Reports (portfolio performance, risk analysis)
•	Customizable Reports
•	Performance Benchmarks (S&P 500, Bitcoin etc.)
•	Export Options (PDF, CSV, Excel)
•	Data Visualization (charts, graphs)
8. Financial Tools and Calculators
•	Investment Calculators (portfolio growth, interest)
•	Risk Assessment Tools
•	Tax Calculation Tools
9. Security Features
•	Security (SSL/TLS Encryption)
•	Multi-factor Authentication (MFA)
•	Audit Logs
10. User Interface (UI) and User Experience (UX)
•	Responsive Design (mobile-friendly)
•	Intuitive Layout
•	Customizable Dashboard (Dark mode optional?)
•	Loading States and Feedback
•	Colour visuals 
11. Integration with External APIs
•	Market Data Integration (real-time stock prices)
•	Banking Integration (deposits/withdrawals)
•	CRM System Integration
12. Support and Help Section
•	Support Page (troubleshooting, help requests)
•	FAQ Section
•	User Guide (Guide for Navigation or a help page)
13. Notifications System
•	In-app Notifications
•	Email Notifications
14. Progressive Web App (PWA)
•	Progressive Web App (PWA) Support
15. Admin Panel (For Website Management)
•	User Management (accounts, permissions)
•	Content Management (static page updates)
16. Verification and Regulatory Tools
•	Customer Verification
•	Trade Compliance with Local Regulations
17. Backup and Disaster Recovery
•	Regular Data Backup
•	Disaster Recovery Plan (Database Backup files)

### Requirements

1. Django – The main framework for the backend.
2. Django REST Framework – For building REST APIs.
3. Django Allauth – For social login integration (if needed).
4. djangorestframework-simplejwt – For token-based authentication (JWT).
5. Firebase Admin SDK – For Firebase integration.
6. Stripe/PayPal SDK – If you need to integrate payment options.

*** Comparison of Django and Flask to choose the optimal framework for the project
| Feature                             | Django                                                 | Flask                                                             |
|-------------------------------------|--------------------------------------------------------|-------------------------------------------------------------------|
| **User Management & Authentication**| Built-in (authentication, authorization, roles)        | Not built-in, requires external libraries (e.g., Flask-Login)     |
| **Admin Interface**                 | Built-in, powerful and customizable                    | Not built-in, requires external libraries (e.g., Flask-Admin)     |
| **Data Management & ORM**           | Built-in (Django ORM)                                  | Not built-in, typically uses SQLAlchemy                           |
| **Security**                        | Built-in protections (CSRF, XSS, SQL injections)       | Minimal built-in protections, requires manual setup or extensions |
| **Scalability & Asynchronicity**    | Supports asynchronous requests, scalable architecture  | Flexible, supports asynchronous behavior with additional setup    |
| **API Support**                     | Built-in (Django REST Framework)                       | Not built-in, but Flask-RESTful can be used                       |
| **Modularity & Code Reuse**         | Modular by design (through apps)                       | Requires manual setup for modularity                              |
| **Payment Integration**             | Easy integration with Stripe, PayPal via libraries     | Not built-in, manual integration with payment systems required    |

***Conclusion:***
Django is better suited for your "ACT (Agentic Corporate Trader)" project because:

It provides built-in solutions for managing users.
The built-in admin interface.
Django REST Framework (DRF) quick option for create of APIs for mobile and web applications.
Django has a good secure, it is very important for a financial applications.
Django’ssupport for asynchronous requests, it is very important for work with large amounts of data and market information.

Flask can be use for smaller microservices or lightweight APIs, but for a centralized backend with complex features and high security needs, Django is the optimal choice.

### Database Configuration

This project utilizes the following database setup:

1. **SQLite**:
   - Purpose: Used for storing system-level data (e.g., user authentication, admin panel, session data).
   - Configuration: Default Django database (`db.sqlite3`).

2. **Firebase Firestore**:
   - Purpose: Used for business logic data (e.g., assets, portfolios, trade history).
   - Configuration: Integrated via Firebase Admin SDK, with credentials stored in the project directory (`config/your-firebase-key.json`).


## Data Model Overview

The system is designed to manage funds and portfolios, allowing Fund Administrators and Fund Managers to create and manage orders for purchasing or selling technology stocks and crypto assets. These orders are processed and managed by the system, with real-time financial data (such as asset prices, trading volume, and financial news) fetched from external APIs.

### 1. **User**
The `User` entity represents the primary actors in the system. There are three roles:
- **System Administrator**: manages the system and users.
- **Fund Administrator**: manages only their own assets (funds and portfolios).
- **Fund Manager**: manages assets for multiple client companies.

#### Fields:
- `id`: Unique identifier for the user.
- `username`: The username for login.
- `password`: Encrypted password for the user.
- `role`: The role of the user (`system_admin`, `fund_admin`, `fund_manager`).

#### Relationships:
- A **Fund Administrator** manages multiple `Funds` and `Portfolios`.
- A **Fund Manager** manages multiple `Clients`, each with their own `Funds` and `Portfolios`.

### 2. **Client**
The `Client` entity represents a company or organization whose assets are managed by a **Fund Manager**. Each client record contains information about the client and their assets.

#### Fields:
- `id`: Unique identifier for the client.
- `name`: The name of the company or organization.
- `fund_manager_id`: The ID of the `User` who acts as the **Fund Manager**.

#### Relationships:
- A `Client` has multiple `Funds`.

### 3. **Fund**
The `Fund` entity represents a pool of financial assets managed by a user. Depending on the user’s role, a fund may belong to either a **Fund Administrator** or a **Client**, managed by a **Fund Manager**.

#### Fields:
- `id`: Unique identifier for the fund.
- `name`: The name of the fund.
- `user_id`: The ID of the `User` (if the fund is managed by a **Fund Administrator**).
- `client_id`: The ID of the `Client` (if the fund is managed by a **Fund Manager**).

#### Relationships:
- A `Fund` contains multiple `Portfolios`.

### 4. **Portfolio**
The `Portfolio` entity represents a collection of financial assets (stocks and cryptocurrencies) owned by a user or client.

#### Fields:
- `id`: Unique identifier for the portfolio.
- `name`: The name of the portfolio.
- `fund_id`: The ID of the `Fund` associated with the portfolio.

#### Relationships:
- A `Portfolio` contains multiple `Assets`.
- A `Portfolio` has multiple `Orders`.

### 5. **Asset**
The `Asset` entity represents individual financial assets (stocks or crypto assets) within a portfolio. It tracks real-time financial data (such as price and volume) through external APIs like Yahoo Finance and Alpha Vantage.

#### Fields:
- `id`: Unique identifier for the asset.
- `symbol`: Ticker symbol of the asset (e.g., `AAPL` for Apple).
- `price`: Current market price of the asset, fetched from external APIs.
- `volume`: The total market trading volume for the asset, fetched from external APIs (not related to the user's specific holdings).
- `amount`: The quantity of the asset held in the portfolio by the user.
- `last_updated`: Date and time of the last price and volume update.
- `portfolio_id`: The ID of the portfolio containing the asset.

#### Relationships:
- An `Asset` belongs to one `Portfolio`.

### 6. **Order**
The `Order` entity represents financial actions (buying or selling) within a portfolio.

#### Fields:
- `id`: Unique identifier for the order.
- `amount`: The quantity of the asset being traded.
- `order_type`: The type of order, either:
  - `buy`: A purchase of an asset.
  - `sell`: A sale of an asset.
- `portfolio_id`: The ID of the portfolio associated with the order.

#### Relationships:
- An `Order` is linked to one `Portfolio`.
- An `Order` may be rated by one `Trade_Rating`.

### 7. **Trade_Rating**
The `Trade_Rating` entity represents a user’s evaluation or rating of a specific order, used to assess the performance of the trade.

#### Fields:
- `id`: Unique identifier for the rating.
- `rating`: The score or evaluation of the order.
- `order_id`: The ID of the associated order.

#### Relationships:
- A `Trade_Rating` is linked to one `Order`.

### 8. **AI_Forecast**
The `AI_Forecast` entity stores predictions or forecasts generated by the system’s AI model. These forecasts help users make informed decisions about their investments.

#### Fields:
- `id`: Unique identifier for the forecast.
- `forecast`: The AI-generated prediction or advice.
- `user_id`: The ID of the `User` who generated the forecast.

#### Relationships:
- An `AI_Forecast` is generated by one `User`.

### 9. **Support_Request**
The `Support_Request` entity allows users to submit inquiries or issues requiring assistance. This can be related to technical or account-related problems.

#### Fields:
- `id`: Unique identifier for the support request.
- `request`: The content of the support request.
- `user_id`: The ID of the `User` who submitted the request.

#### Relationships:
- A `Support_Request` is submitted by one `User`.

### Integration with External APIs
- **Yahoo Finance API** and **Alpha Vantage API** are integrated to fetch real-time data such as stock prices, trading volume, and financial news. The system regularly updates this data to ensure accurate information is available to users.
- **Stock Prices and Volume**: The `Asset` entity uses real-time price data from external APIs to keep portfolios up to date. Each order records the volume of traded assets.
- **Financial News**: The system can display relevant financial news related to assets using Yahoo Finance, allowing users to stay informed about events that may impact their investments.

---

### Integration with External APIs:

- **Yahoo Finance API** and **Alpha Vantage API** are used to fetch real-time data for investments, including stock prices, trading volume, and **financial news**. These APIs keep the system updated with real-world data that allows Fund Managers and Administrators to make well-informed decisions.
  
- **Financial News**: By integrating with the Yahoo Finance API, the system can display relevant financial news related to a user’s investments, helping them stay informed of market events that could impact their assets.

--- 

### Database Diagram

The ACT system's database structure represents the relationships between key entities such as Users, Clients, Funds, Portfolios, and financial Assets. Below is a summary of the database structure, which includes managing orders, tracking assets, work with AI, and integrating with external APIs for real-time financial data.

### Key Entities:

- **User**: Represents system actors, including Fund Administrators, Fund Managers, and System Administrators.
- **Client**: A company or organization whose assets are managed by a Fund Manager.
- **Fund**: A collection of assets managed by a User (either a Fund Administrator or Client managed by a Fund Manager).
- **Portfolio**: A collection of assets within a fund, managed by a User or Client.
- **Asset**: Financial assets (stocks or crypto) tracked within a portfolio, with real-time data fetched from external APIs.
- **Order**: Represents buy or sell transactions within a portfolio.
- **Trade Rating**: User's evaluation of an order's performance.
- **AI Forecast**: Predictive financial insights generated by the AI engine.
- **Support Request**: A user's inquiry for technical or account-related issues requiring assistance.

### Relationships:

- A **User** manages multiple **Funds** and **Portfolios**.
- A **Fund** contains multiple **Portfolios**.
- A **Portfolio** contains multiple **Assets** and **Orders**.
- Each **Order** may be rated by one **Trade Rating**.
- **AI Forecasts** are generated by **Users**.
- **Support Requests** are submitted by **Users**.

### Key Relationships Explained:

- **User and Fund**: A user can manage multiple funds. For example, a **Fund Manager** could oversee various funds belonging to different clients.
- **User and Portfolio**: Each **User** can own multiple portfolios, especially **Fund Administrators** who are handling their own investments.
- **Client and Fund**: A **Client** can have multiple funds managed on their behalf by a **Fund Manager**.
- **Portfolio and Asset**: Each portfolio contains several assets, representing individual stocks or crypto assets that the user has invested in.
- **Order and Portfolio**: Users can create multiple orders (buy or sell) for assets within their portfolios.
- **Order and Trade Rating**: Each order can be rated based on the performance of the trade.
- **AI Forecast**: Generated by the AI engine to assist users in making informed investment decisions.
- **Support Request**: Users can submit support requests if they require assistance with their portfolios or technical issues.

![Database Diagram](/database-diagram.png)

[Diagram Code in PlantUML](https://www.plantuml.com/plantuml/uml/):

```txt
@startuml
class User {
  +id: int
  +username: string
  +password: string
  +role: string
}

class Client {
  +id: int
  +name: string
  +fund_manager_id: int
}

class Fund {
  +id: int
  +name: string
  +user_id: int
  +client_id: int
}

class Portfolio {
  +id: int
  +name: string
  +fund_id: int
}

class Asset {
  +id: int
  +symbol: string
  +price: float
  +volume: int
  +amount: float
  +last_updated: datetime
  +portfolio_id: int
}

class Order {
  +id: int
  +amount: float
  +order_type: string
  +portfolio_id: int
}

class Trade_Rating {
  +id: int
  +rating: float
  +order_id: int
}

class AI_Forecast {
  +id: int
  +forecast: string
  +user_id: int
}

class Support_Request {
  +id: int
  +request: string
  +user_id: int
}

' Relationships
User "1" -- "many" Fund : manages
User "1" -- "many" Portfolio : owns
User "1" -- "many" AI_Forecast : generates
User "1" -- "many" Support_Request : submits

Client "1" -- "many" Fund : manages

Fund "1" -- "many" Portfolio : contains
Portfolio "1" -- "many" Asset : contains
Portfolio "1" -- "many" Order : has

Order "1" -- "1" Trade_Rating : rated by

@enduml

```

### Backend

#### Development Server on the DigitalOcean host

The project is currently running on a development server accessible via the following address:

```bash
http://161.35.38.50:8000
```

You can access both the API and the Django Admin interface using this URL.

- **Django Admin**: To access the admin panel, navigate to `/admin/` on the server URL (e.g., `http://161.35.38.50:8000/admin/`).

- **API Endpoints**: The API can be accessed by using the `/api/`, for example

  - **User Registration**: 
    ```bash
    POST http://161.35.38.50:8000/api/register/
    ```

#### Backend-Installation-Guide for local machine 
To set up the backend of the ACT (Agentic Corporate Trader) project on your local machine, follow these steps:
1. ***Clone the Repository***
    ```bash
    git clone https://github.com/your-repo/Project2024.git
    cd Project2024/backend
    ```
2. ***Set Up Virtual Environment***
    ```bash
    # For Windows
    python -m venv venv

    # For Mac/Linux
    python3 -m venv venv
    ```
3. ***Activate the virtual environment:***
    ```bash
    # For Windows
    venv\Scripts\activate

    # For Mac/Linux
    source venv/bin/activate
    ```
4. ***Install Dependencies***
    ```bash
    pip install -r requirements.txt
    ```
5. ***Firebase Setup***
    
    The project uses Firebase as a database for specific assets and trade-related data. To integrate Firebase:

    Go to the Firebase Console and download the Firebase Admin SDK credentials JSON file.
    Place the downloaded JSON file in the config/ directory in the project root.
    Ensure the path to the Firebase credentials file is correctly set in the settings.py file.
    
    Example path in settings.py:
    ```python
    FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'config', 'your-firebase-key.json')
    ```
6. ***Database Setup***
    For local development, the project uses SQLite. If you are starting fresh or have unapplied migrations, run the following commands to apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
7. ***Create a Superuser***
    To access the Django admin interface, you need to create a superuser:
    ```bash
    python manage.py createsuperuser
    ```
8. ***Running the Development Server***
    ```bash
    python manage.py runserver
    ```
    The backend will be available at http://127.0.0.1:8000/

---

### Work in admin panel

1) ***Creating Fund Administrator or Fund Manager from admin panel***
    You can to add users with the roles **Fund Administrator** and **Fund Manager** through the Django admin interface:

    1. Go to the admin panel at `{{url}}/admin/`.
    2. Log in using your superuser credentials.
    3. Navigate to **CORE > Users** and add new users. You can assign them the roles **Fund Administrator** or **Fund Manager** as needed.
    4. **Ensure** that the **is_staff** and **is_active** flags are checked for the users you create. This allows them to log in and interact with the system.
    5. After creating the users, you can authenticate them via the API.

---

### Permissions in Project

In this project, **role-based permissions** are enforced to provide secure and restricted access to various endpoints. The following roles have been defined for the system:

---

## Role Definitions

1. **FundAdmin**:
   - Fund Administrators can manage assets and subscriptions associated with their own funds.
   - They have access to create, read, update, and delete operations within their own scope.

2. **FundManager**:
   - Fund Managers can manage client assets, subscriptions, and funds for multiple clients.
   - They have broader permissions compared to Fund Administrators.

---

### API

#### ***User Registration Endpoint***
This endpoint allows for the registration of new users with specific roles, such as Fund Administrator or Fund Manager.

To register a new user, send a POST request to:
```bash
POST /api/register/
```

With the following fields in the request body:
```json
{
    "username": "admin001",
    "email": "admin001@example.com",
    "password": "password_123",
    "role": "fund_admin"
}
```

For example:
```json
POST /api/register/
HTTP 201 Created
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "username": "Admin001",
    "email": "admin001@example.com",
    "password": "password_123",
    "role": "fund_admin"
}
```

Example Responses: 

1) Status: 201 Created

```json
{
    "user": {
        "username": "Manager004",
        "email": "manager004@example.com",
        "role": "fund_manager"
    },
    "refresh": "eyJhbGciOiJIUzI1....z0Lb9o4syqXDB4kzA",
    "access": "eyJhbGciOiJI.............8hFCgOmlBXTr_4"
}
```

2) Status: 400 Bad Request
```json
{
  "error": "User already exists or invalid data"
}
```

#### ***API Authentication***

The project uses JWT (JSON Web Tokens) for authentication. 

To obtain JWT tokens, send a POST request to:
```bash
POST /api/token/
```

With **Fund Administrator** or **Fund Manager** credentials in the request body:
```json
{
    "email": "user@emai.com",
    "password": "password"
}
```

This will return access and refresh tokens, which are used to authenticate API requests. 

For example:
```bash
POST /api/token/
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXV...hEdGfvcfWZk6mZa0ftLU3AOPyFDZHI",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVC...-Rl2Tc57Kkp_MzuH0jxg0APRrDr9o9s"
}
```

### Asset Management

#### Retrieve All Assets

Endpoint: ``GET /api/assets/``

Description: ``Fetches a list of all assets.``

Example Request:
```bash
curl -X GET 'http://161.35.38.50:8000/api/assets/' -H 'Authorization: Bearer JWT_TOKEN'
```

Example Response (Status 200):
```json
[
    {
        "id": "asset_id_1",
        "symbol": "AAPL",
        "price": 150.5,
        "volume": 2000,
        "amount": 100,
        "portfolio_id": "portfolio_id_1",
        "last_updated": "2024-11-02T12:34:56Z"
    },
    ...
]
```

#### Create an Asset

Endpoint: ``POST /api/assets/``

Description: ``Creates a new asset.``

Request Body:
```json
{
    "symbol": "AAPL",
    "price": 150.5,
    "volume": 2000,
    "amount": 100,
    "portfolio_id": "portfolio_id_1"
}
```

Example Request:

```bash
curl -X POST 'http://161.35.38.50:8000/api/assets/' -H 'Authorization: Bearer JWT_TOKEN' -d '{"symbol": "AAPL", "price": 150.5, "volume": 2000, "amount": 100, "portfolio_id": "portfolio_id_1"}'
```

Example Response (Status 201 Created):
```json
{
    "id": "asset_id_1",
    "symbol": "AAPL",
    "price": 150.5,
    "volume": 2000,
    "amount": 100,
    "portfolio_id": "portfolio_id_1",
    "last_updated": "2024-11-02T12:34:56Z"
}
```

#### Retrieve a Specific Asset by ID

Endpoint: ``GET /api/assets/<asset_id>/``

Description: ``Fetches details of a specific asset by its ID.``

Example Request:
```bash
curl -X GET 'http://161.35.38.50:8000/api/assets/asset_id_1/' -H 'Authorization: Bearer JWT_TOKEN'
```

Example Response (Status 200):
```json
{
    "id": "asset_id_1",
    "symbol": "AAPL",
    "price": 150.5,
    "volume": 2000,
    "amount": 100,
    "portfolio_id": "portfolio_id_1",
    "last_updated": "2024-11-02T12:34:56Z"
}
```

#### Update an Existing Asset

Endpoint: ``PUT /api/assets/<asset_id>/``

Description: ``Updates an existing asset's details.``

Request Body:
```json
{
    "symbol": "AAPL",
    "price": 160.0,
    "volume": 2500,
    "amount": 120
}
```

Example Request:
```bash
curl -X PUT 'http://161.35.38.50:8000/api/assets/asset_id_1/' -H 'Authorization: Bearer JWT_TOKEN' -d '{"symbol": "AAPL", "price": 160.0, "volume": 2500, "amount": 120}'
```

Example Response (Status 200):
```json
{
    "id": "asset_id_1",
    "symbol": "AAPL",
    "price": 160.0,
    "volume": 2500,
    "amount": 120,
    "portfolio_id": "portfolio_id_1",
    "last_updated": "2024-11-03T12:34:56Z"
}
```

#### Delete an Asset

Endpoint: ``DELETE /api/assets/<asset_id>/``

Description: ``Deletes a specific asset.``

Example Request:
```bash
curl -X DELETE 'http://161.35.38.50:8000/api/assets/asset_id_1/' -H 'Authorization: Bearer JWT_TOKEN'
```

Example Response (Status 204 No Content):
```json
{}
```

### Client Management
- **GET** `/api/clients/` - Retrieve all clients.
- **POST** `/api/clients/` - Create a new client.
- **GET** `/api/clients/<client_id>/` - Retrieve a specific client by its ID.
- **PUT** `/api/clients/<client_id>/` - Update an existing client.
- **DELETE** `/api/clients/<client_id>/` - Delete a client.

### Fund Management
- **GET** `/api/funds/` - Retrieve all funds.
- **POST** `/api/funds/` - Create a new fund.
- **GET** `/api/funds/<fund_id>/` - Retrieve a specific fund by its ID.
- **PUT** `/api/funds/<fund_id>/` - Update an existing fund.
- **DELETE** `/api/funds/<fund_id>/` - Delete a fund.

### Portfolio Management
- **GET** `/api/portfolios/` - Retrieve all portfolios.
- **POST** `/api/portfolios/` - Create a new portfolio.
- **GET** `/api/portfolios/<portfolio_id>/` - Retrieve a specific portfolio by its ID.
- **PUT** `/api/portfolios/<portfolio_id>/` - Update an existing portfolio.
- **DELETE** `/api/portfolios/<portfolio_id>/` - Delete a portfolio.

### Order Management
- **GET** `/api/orders/` - Retrieve all orders.
- **POST** `/api/orders/` - Create a new order.
- **GET** `/api/orders/<order_id>/` - Retrieve a specific order by its ID.
- **PUT** `/api/orders/<order_id>/` - Update an existing order.
- **DELETE** `/api/orders/<order_id>/` - Delete an order.

### Trade Rating Management
- **GET** `/api/trade-ratings/` - Retrieve all trade ratings.
- **POST** `/api/trade-ratings/` - Create a new trade rating.
- **GET** `/api/trade-ratings/<trade_rating_id>/` - Retrieve a specific trade rating by its ID.
- **PUT** `/api/trade-ratings/<trade_rating_id>/` - Update an existing trade rating.
- **DELETE** `/api/trade-ratings/<trade_rating_id>/` - Delete a trade rating.

### AI Forecast Management
- **GET** `/api/ai-forecasts/` - Retrieve all AI forecasts.
- **POST** `/api/ai-forecasts/` - Create a new AI forecast.
- **GET** `/api/ai-forecasts/<forecast_id>/` - Retrieve a specific AI forecast by its ID.
- **PUT** `/api/ai-forecasts/<forecast_id>/` - Update an existing AI forecast.
- **DELETE** `/api/ai-forecasts/<forecast_id>/` - Delete an AI forecast.

### Support Request Management
- **GET** `/api/support-requests/` - Retrieve all support requests.
- **POST** `/api/support-requests/` - Create a new support request.
- **GET** `/api/support-requests/<support_request_id>/` - Retrieve a specific support request by its ID.
- **PUT** `/api/support-requests/<support_request_id>/` - Update an existing support request.
- **DELETE** `/api/support-requests/<support_request_id>/` - Delete a support request.

### External APIs Integration

In this project, we have integrated two external financial APIs: Yahoo Finance and Alpha Vantage. These APIs allow the application to retrieve real-time and historical market data for stocks and other financial instruments.


#### Yahoo Finance API:

The Yahoo Finance API provides real-time stock prices, market data, and other financial insights. We use this API to get information such as the current price of stocks, market sentiment, and trading volumes.

**URL:** `/api/yahoo-finance/`

**Request Method:** `GET`

**Request Parameters:**
- `ticker`: The stock ticker symbol (e.g., `AAPL` for Apple Inc.).
- `type`: The type of asset (e.g., `STOCKS`).

```bash
curl -X GET 'http://161.35.38.50:8000/api/yahoo-finance/?ticker=AAPL&type=STOCKS' \
-H 'Authorization: Bearer JWT_TOKEN'
```

**Example Response:**

```json
{
    "meta": {
        "version": "v1.0",
        "status": 200,
        "copywrite": "https://apicalls.io"
    },
    "body": {
        "symbol": "AAPL",
        "companyName": "Apple Inc. Common Stock",
        "stockType": "Common Stock",
        "exchange": "NASDAQ-GS",
        "primaryData": {
            "lastSalePrice": "$227.55",
            "netChange": "-1.49",
            "percentageChange": "-0.65%",
            "deltaIndicator": "down",
            "lastTradeTimestamp": "Oct 13, 2024",
            "isRealTime": true,
            "bidPrice": "N/A",
            "askPrice": "N/A",
            "bidSize": "N/A",
            "askSize": "N/A",
            "volume": "31,759,188",
            "currency": null
        },
        "secondaryData": null,
        "marketStatus": "Closed",
        "assetClass": "STOCKS",
        "keyStats": {
            "fiftyTwoWeekHighLow": {
                "label": "52 Week Range:",
                "value": "164.08 - 237.23"
            },
            "dayrange": {
                "label": "High/Low:",
                "value": "NA"
            }
        }
    }
}
```

#### Yahoo Finance News API:

The Yahoo News API endpoint in our backend allows fetching real-time financial up-to-date market news, trends, and insights from the Yahoo Finance service.

**URL:** `/api/yahoo-news/`

**Request Method:** `GET`

**Request Parameters:**
- `ticker`: The stock ticker symbol (e.g., `AAPL` for Apple Inc.).
- `type`: The type of asset (`ALL`, `VIDEO` or `PRESS_RELEASE`).

```bash
curl -X GET http://161.35.38.50:8000/api/yahoo-news/ \
-H "Authorization: Bearer JWT_TOKEN" \
-H "Content-Type: application/json" \
-d "tickers=AAPL&type=ALL"
```

**Example Response:**

```json
{
    "meta": {
        "version": "v1.0",
        "status": 200,
        "copywrite": "https://apicalls.io",
        "total": 50
    },
    "body": [
        {
            "url": "https://www.cnbc.com/2024/11/19/qualcomm-says-it-expects-4-billion-in-pc-sales-by-2029.html",
            "img": "https://cdn.snapi.dev/images/v1/o/w/m/qcomm14-2450117-2767892.jpg",
            "title": "Qualcomm says it expects $4 billion in PC chip sales by 2029",
            "text": "Qualcomm said at its investor day on Tuesday...",
            "source": "CNBC",
            "type": "Article",
            "tickers": ["$QCOM"],
            "time": "Nov 19, 2024, 4:49 PM EST",
            "ago": "6 minutes ago"
        },
        {
            "url": "https://www.youtube-nocookie.com/embed/q8qdLAb0nMo",
            "img": "https://cdn.snapi.dev/images/v1/m/i/6/nvda19-2686814-2767903.jpg",
            "title": "What Nvidia's Blackwell means for 2025 AI chip demand",
            "text": "Nvidia (NVDA) prepares to report fiscal third quarter earnings...",
            "source": "Yahoo Finance",
            "type": "Video",
            "tickers": ["$NVDA"],
            "time": "Nov 19, 2024, 4:48 PM EST",
            "ago": "7 minutes ago"
        }
    ]
}
```

**Response Fields:**

- **`meta`**: Metadata about the API call.
  - **`version`**: API version.
  - **`status`**: HTTP status code.
  - **`total`**: Total number of articles retrieved.

- **`body`**: A list of news articles.
  - **`url`**: The link to the full news article or video.
  - **`img`**: URL to the thumbnail image.
  - **`title`**: Title of the article or video.
  - **`text`**: A brief description of the content.
  - **`source`**: The source of the news (e.g., CNBC, Reuters).
  - **`type`**: Type of content (`ALL` or `VIDEO` or `PRESS_RELEASE`).
  - **`tickers`**: Associated stock tickers.
  - **`time`**: Published date and time.
  - **`ago`**: How long ago the news was published.

**Common Use Cases:**

1. Fetch All News: Retrieve all available financial news.
```bash
curl -X GET http://161.35.38.50:8000/api/yahoo-news/ \
-H "Authorization: Bearer JWT_TOKEN"
```

2. Fetch News by Tickers: Retrieve news related to specific companies or assets.
```bash
curl -X GET http://161.35.38.50:8000/api/yahoo-news/?tickers=AAPL,MSFT \
-H "Authorization: Bearer JWT_TOKEN"
```

3. Filter by Content Type: Fetch only videos or articles.
```bash
curl -X GET http://161.35.38.50:8000/api/yahoo-news/?type=VIDEO \
-H "Authorization: Bearer JWT_TOKEN"
```

**Error Handling:**

* **401 Unauthorized:** Ensure your token is valid and included in the Authorization header.
* **400 Bad Request:** Verify that query parameters are correctly formatted.
* **503 Service Unavailable:** Yahoo API service is down or unreachable.


#### Alpha Vantage API:

The Alpha Vantage API provides historical and real-time stock data, including daily time series, which shows the open, high, low, close prices, and volume for each day. This is particularly useful for performing technical analysis or retrieving historical trends of a stock.

**URL:** `/api/alpha-vantage/`

**Request Method:** `GET`

**Request Parameters:**
- `symbol`: The stock ticker symbol (e.g., `AAPL` for Apple Inc.).
- `function`: The type of time series data (e.g., TIME_SERIES_DAILY).
- `outputsize`: Data size, either compact (latest 100 data points) or full (all available data).

```bash
curl -X GET 'http://161.35.38.50:8000/api/alpha-vantage/?symbol=AAPL' \
-H 'Authorization: Bearer JWT_TOKEN'
```

**Example Response:**

```json
{
    "Meta Data": {
        "1. Information": "Daily Prices (open, high, low, close) and Volumes",
        "2. Symbol": "IBM",
        "3. Last Refreshed": "2024-10-11",
        "4. Output Size": "Compact",
        "5. Time Zone": "US/Eastern"
    },
    "Time Series (Daily)": {
        "2024-10-11": {
            "1. open": "233.2500",
            "2. high": "233.4400",
            "3. low": "230.4600",
            "4. close": "233.2600",
            "5. volume": "3469322"
        },
        "2024-10-10": {
            "1. open": "235.1000",
            "2. high": "235.8300",
            "3. low": "231.8100",
            "4. close": "233.0200",
            "5. volume": "3142031"
        },
        ...
        "2024-05-21": {
            "1. open": "169.9400",
            "2. high": "174.9700",
            "3. low": "169.9400",
            "4. close": "173.4700",
            "5. volume": "6459800"
        }
    }
}
```

#### AI-Powered Predict API:

The Predict API endpoint provides stock prediction data based on AI analysis.

**URL:** `/api/act-ai/predict/`

**Request Method:** `POST`

**Request Body:**
- `symbol`: The stock ticker symbol (e.g., `AAPL` for Apple Inc.).

```bash
curl -X POST http://localhost:8000/api/act-ai/predict/ \
-H "Authorization: Bearer JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{"symbol": "AAPL"}'
```

**Example Response:**

```json
{
  "id": 1,
  "forecast": "**AAPL Short-Term Trading Analysis**\n\n**Time of Analysis:** December 4, 2024, 01:09 AM GMT\n\n**Disclaimer:** This analysis is based on hypothetical real-time data provided and is for illustrative purposes only. It does not constitute financial advice. Trading involves risk, and losses can exceed your investment. Always conduct your own thorough research and consider consulting a financial advisor before making any investment decisions.\n\n**1. Price Action Analysis:**\n\n- **Current Trend Direction and Strength:** The current price of $243.00 shows a slight uptrend from the previous day's close of $229.00. However, the net change is minimal (0.14%), suggesting weak momentum. After-hours trading might show temporary fluctuation, and a more robust trend assessment requires observing the opening price and subsequent price action during regular trading hours.\n\n- **Price Momentum Indicators:** Without access to real-time data for momentum indicators like RSI (Relative Strength Index) or MACD (Moving Average Convergence Divergence), a precise assessment is not possible. These indicators would help confirm the strength and sustainability of the current trend.\n\n- **Support/Resistance Levels from Current Price Action:** Immediate support could be found around $238.9 (today's low), while resistance might be encountered near $242.75 (today's high). More robust support and resistance levels would be identified by examining longer-term charts and previous significant high and low points.\n\n- **Significance of the Current Bid/Ask Spread:** The bid/ask spread of $242.74/$242.95 ($0.21) is relatively tight, suggesting relatively good liquidity, making it easier to enter and exit trades. However, it doesn't reveal anything conclusive about the immediate buying or selling pressure.\n\n**2. Volume Analysis:**\n\n- **Volume Trend Analysis:** Current volume (38,861,014) is significantly higher than the previous day's volume (3,138,952). This increased volume could indicate heightened investor interest and potentially stronger price movements. Volume will be crucial in determining the trend's strength. If the price increase is accompanied by above-average volume, it suggests strong buying pressure. If volume decreases while prices rise, it could indicate a weakening buying momentum.\n\n- **Unusual Volume Activity Assessment:** The drastically higher volume today compared to yesterday warrants further investigation for any news or events driving this increased activity.\n\n**3. Trading Range Analysis:**\n\n- **Key Levels within Today's Range:** $238.9 (low) and $242.75 (high) are significant intraday levels. Breaks above $242.75 or below $238.9 could signal further price movements in that direction.\n\n- **Position Relative to 52-Week Range:** The current price of $243 is relatively high compared to the 52-week low of $164.08 but significantly below the 52-week high of $240.79, suggesting potential for further upward movement, but cautious approach is suggested.\n\n- **Breakout/Breakdown Potential:** A decisive break above $242.75 could signal a potential short-term uptrend. Conversely, a break below $238.9 could signal a possible short-term downturn.\n\n- **Price Volatility Assessment:** The relatively small range between today's high and low compared to the 52-week range indicates relatively low volatility for now. However, this could change rapidly.\n\n**4. Market Context:**\n\n- **Current Market Phase:** The overall market phase (bullish, bearish, or sideways) is not provided. This crucial context is needed for a more comprehensive analysis.\n\n- **Trading Session Analysis:** The data is from the after-hours trading session. This period can experience increased volatility due to lower liquidity and is not always representative of the regular trading session's price action.\n\n- **Exchange-Specific Considerations:** The stock trades on NASDAQ-GS, a well-established and liquid exchange.\n\n- **Real-time vs. Delayed Data Implications:** Using real-time data is crucial for short-term trading opportunities. Delayed data will not suffice.\n\n**5. Short-Term Opportunities:**\n\nBased on the limited data, identifying concrete short-term trading opportunities is difficult. A more complete picture requires:\n\n- **Real-time data for momentum indicators (RSI, MACD):** This will confirm the trend's strength and potential reversal points.\n- **Extended historical price data:** This will provide more comprehensive support and resistance levels.\n- **News and events affecting AAPL:** This will explain any unusual volume activity.\n- **Market-wide conditions:** This provides the proper context to the stock's movement.\n\n**Hypothetical Trading Scenario (Illustrative Only):**\n\n- **If the price decisively breaks above $243.50 (slightly above today's high) with increased volume:** This might signal a short-term bullish opportunity.\n  - **Entry Point:** $243.75\n  - **Stop-Loss:** $242.50\n  - **Target:** $245.00 (risk-reward of approximately 1:1)\n\n- **If the price decisively breaks below $238.00 (slightly below today's low) with increased volume:** This might signal a short-term bearish opportunity.\n  - **Entry Point:** $237.75\n  - **Stop-Loss:** $238.50\n  - **Target:** $236.00 (risk-reward of approximately 1:1)\n\n**Confidence Level:** Low. The analysis is highly limited by the absence of vital data. The confidence level would increase significantly with more complete real-time and historical data, including technical indicators and fundamental analysis.\n\n**Short-Term Price Targets:** Given the limited data, providing specific price targets is unreliable. More complete analysis is necessary.\n\n**Note:** This analysis is purely hypothetical due to the limitations in available data. It's crucial to use up-to-date and comprehensive data for making real trading decisions.",
  "user_id": 2
}
```

**Response Fields:**

- **`forecast`**: AI prediction results.
  - **`price`**: Predicted stock price.
  - **`confidence`**: AI model confidence in the prediction (percentage).

**Error Handling:**

* **401 Unauthorized:** Ensure your token is valid and included in the Authorization header.
* **400 Bad Request:** Ensure ``symbol`` is included in the request body.
* **503 Service Unavailable:** Yahoo API service is down or unreachable.


#### AI-Powered History API:

The History API endpoint provides historical stock data for the specified stock symbol.

**URL:** `/api/act-ai/history/`

**Request Method:** `GET`

**Request Parameters:**
- `symbol`: The stock ticker symbol (e.g., `AAPL` for Apple Inc.).

```bash
curl -X GET "http://localhost:8000/api/act-ai/history/?symbol=AAPL" \
-H "Authorization: Bearer JWT_TOKEN"
```

**Example Response:**

```json
{
    "history": [
        {"date": "2024-12-01", "price": 205.5},
        {"date": "2024-12-02", "price": 207.0}
    ]
}
```

**Response Fields:**

- **`history`**: Historical stock price data.
  - **`date`**: Date of the historical price.
  - **`price`**: Closing price of the stock on the given date.

**Error Handling:**

* **401 Unauthorized:** Ensure your token is valid and included in the Authorization header.
* **400 Bad Request:** Ensure ``symbol`` query parameter is included.


#### AI-Powered Trade Rating Endpoint:

This AI-powered endpoint provides the trade rating information for a given stock symbol. The trade rating is based on various analytics and insights related to the specified symbol.

**URL:** `/api/act-ai/trade-rating/`

**Request Method:** `GET`

**Request Parameters:**
- `symbol` (required): The stock ticker symbol (e.g., `AAPL` for Apple Inc.).

```bash
curl -X GET "http://localhost:8000/api/act-ai/trade-rating/?symbol=AAPL" \
-H "Authorization: Bearer JWT_TOKEN"
```

**Response:**

Returns an object with the trade rating details for the given stock symbol.

**Example Response:**

```json
{
  "symbol": "AAPL",
  "rating": {
    "overall": 8.5,
    "technical": 7.8,
    "fundamental": 9.2,
    "sentiment": 8.0
  },
  "updated_at": "2024-12-11T10:00:00Z"
}
```

**Error Handling:**

* **401 Unauthorized:** Ensure your token is valid and included in the Authorization header.
* **400 Bad Request:** Ensure ``symbol`` query parameter is included.


#### Fetch Stock Data from Finnhub

This endpoint allows fetching stock market data for a given stock symbol using the Finnhub API.

**URL:** `/api/act-ai/stock-data/`

**Request Method:** `GET`

**Request Parameters:**
- `symbol`: The stock ticker symbol (e.g., `AAPL` for Apple Inc.).

```bash
curl -X GET "http://localhost:8000/api/act-ai/stock-data/?symbol=AAPL" \
-H "Authorization: Bearer JWT_TOKEN"
```

**Example Response:**

```json
{
    "c": 247.77,
    "d": 1.02,
    "dp": 0.4134,
    "h": 248.21,
    "l": 245.34,
    "o": 246.89,
    "pc": 246.75,
    "t": 1733864400
}
```

**Error Handling:**

* **401 Unauthorized:** Ensure your token is valid and included in the Authorization header.
* **400 Bad Request:** Ensure ``symbol`` query parameter is included.
* **503 Service Unavailable:** Finnhub API service is down or unreachable.


#### Fetch News from Finnhub

This endpoint retrieves the latest news articles for a specific category from Finnhub.

**URL:** `/api/act-ai/stock-news/`

**Request Method:** `GET`

**Request Parameters:**
- `category`: (Optional) News category (e.g., `general`, `crypto`). Default is `general`.

```bash
curl -X GET "http://localhost:8000/api/act-ai/stock-news/?category=general" \
-H "Authorization: Bearer JWT_TOKEN"
```

**Example Response:**

```json
[
    {
        "category": "general",
        "datetime": 1733864400,
        "headline": "Stock market trends today",
        "id": 12345,
        "image": "https://example.com/image.jpg",
        "related": "AAPL",
        "source": "Finnhub",
        "summary": "An overview of today's stock market performance.",
        "url": "https://example.com/news/12345"
    },
    ...
]
```

**Error Handling:**

* **401 Unauthorized:** Ensure your token is valid and included in the Authorization header.
* **400 Bad Request:** Ensure ``symbol`` query parameter is included.
* **503 Service Unavailable:** Finnhub API service is down or unreachable.


#### Trending Coins Endpoint from CoinGecko

This endpoint retrieves a list of trending cryptocurrencies, including their detailed market data, price changes, rankings, and additional information using CoinGecko.

**URL:** `/api/act-ai/trending-coins/`

**Request Method:** `GET`

**Request Parameters:**
- `coin_id`: (Optional) The ID of the cryptocurrency (e.g., `bitcoin`, `ethereum`). Default is `bitcoin`.

```bash
curl -X GET "http://localhost:8000/api/act-ai/trending-coins/" \
-H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**

A JSON array containing trending coins. Each object includes the following fields:

* `id`: The unique identifier for the coin.
* `name`: The name of the cryptocurrency.
* `symbol`: The ticker symbol of the cryptocurrency.
* `market_cap_rank`: The current ranking based on market capitalization.
* `price`: Current price in USD.
* `price_btc`: Current price in BTC.
* `price_change_percentage_24h`: The percentage price change in the last 24 hours for various currencies.
* `market_cap`: The current market capitalization of the cryptocurrency.
* `total_volume`: The total trading volume in USD over the last 24 hours.
* `sparkline`: A URL to a sparkline chart representing the price changes over time.
* `thumb`, `small`, `large`: URLs for different sizes of the cryptocurrency's logo.

**Example Response:**

```json
{
    "coins": [
        {
            "item": {
                "id": "vita-inu",
                "name": "Vita Inu",
                "symbol": "VINU",
                "market_cap_rank": 918,
                "price": 5.110131718661772e-08,
                "price_btc": "0.000000000000528258635215761",
                "price_change_percentage_24h": {
                    "usd": -9.777662743078121,
                    "btc": -9.125630280198598,
                    "eth": -7.593784806228662
                },
                "market_cap": "$46,018,123",
                "total_volume": "$13,096,062",
                "sparkline": "https://www.coingecko.com/coins/20594/sparkline.svg",
                "thumb": "https://coin-images.coingecko.com/coins/images/20594/standard/vita-inu.png",
                "small": "https://coin-images.coingecko.com/coins/images/20594/small/vita-inu.png",
                "large": "https://coin-images.coingecko.com/coins/images/20594/large/vita-inu.png"
            }
        },
        ...
    ]
}
```

**Error Handling:**

* **401 Unauthorized:** Ensure your token is valid and included in the Authorization header.
* **503 Service Unavailable:** CoinGecko API service is down or unreachable.


#### Get Cryptocurrency Information from CoinGecko

This endpoint provides detailed information about a specific cryptocurrency. It allows users to retrieve data such as the cryptocurrency's current price, market capitalization, trading volume, and other relevant details by specifying its unique identifier or symbol using CoinGecko.

**URL:** `/api/act-ai/coin-data/`

**Request Method:** `GET`

**Request Parameters:**
- `coin_id` (required): The unique identifier of the cryptocurrency, e.g., `bitcoin`.

```bash
curl -X GET "http://localhost:8000/api/act-ai/coin-data/?coin_id=bitcoin" \
-H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**

A JSON array containing trending coins. Each object includes the following fields:

* `id`: Unique identifier of the cryptocurrency (e.g., `bitcoin`).
* `symbol`: Cryptocurrency symbol (e.g., `btc`).
* `name`: Full name of the cryptocurrency.
* `web_slug`: Unique identifier used for URLs.
* `hashing_algorithm`: Hashing algorithm used by the cryptocurrency (e.g., `SHA-256`).
* `categories`: Categories the cryptocurrency belongs to (e.g., `Cryptocurrency`, `Proof of Work`).
* `description`: A description of the cryptocurrency (available in multiple languages).
* `localization`: Localized names of the cryptocurrency.
* `links`: Official resource links, including the website, whitepaper, forums, etc.
* `market_data`: Market data including current price, market capitalization, trading volume, and more.

**Example Response:**

```json
{
  "id": "bitcoin",
  "symbol": "btc",
  "name": "Bitcoin",
  "web_slug": "bitcoin",
  "hashing_algorithm": "SHA-256",
  "categories": ["Cryptocurrency", "Proof of Work"],
  "description": {
    "en": "Bitcoin is the first successful internet money...",
    "ru": "Биткоин — это первая успешная интернет-валюта..."
  },
  "localization": {
    "en": "Bitcoin",
    "ru": "Биткоин"
  },
  "links": {
    "homepage": ["https://bitcoin.org"],
    "whitepaper": "https://bitcoin.org/bitcoin.pdf"
  },
  "market_data": {
    "current_price": {
      "usd": 96412,
      "eur": 91560
    },
    "market_cap": {
      "usd": 1910526095727,
      "eur": 1814390333117
    },
    "total_volume": {
      "usd": 143027804177
    }
  }
}
```

**Error Handling:**

* **401 Unauthorized:** Ensure your token is valid and included in the Authorization header.
* **400 Bad Request**: The `coin_id` parameter is missing or invalid.
* **503 Service Unavailable:** CoinGecko API service is down or unreachable.

#### Stripe Integration Endpoints

1. **Payment for Subscription (Annual or Monthly)**

    **URL:** `/api/create-checkout-session/`  
    **Method:** `POST`  
    **Permissions:** Only users with roles **FundAdmin** or **FundManager**.

    **Description:**
    This endpoint creates a Stripe Checkout session for processing subscription payments. It supports both annual and monthly plans.

**Request (JSON):**
```json
{
  "price_id": "price_1QX8TOP9tIxdtAMKjWZcQIu6",
  "email": "customer@example.com"
}
```
* `price_id`: `Stripe Price ID` for the subscription plan (annual or monthly).
* `email`: User's email to associate the subscription with a `Stripe Customer`.

**Response (Success):**
```json
{
  "sessionId": "cs_test_a1b2c3d4e5f6g7h8i9j0"
}
```

**Response (Error):**
```json
{
  "error": "Invalid price ID or email."
}
```

**Notes:**
* After receiving the `sessionId`, redirect the user to `Stripe Checkout` for completing the payment:
    ```javascript
    stripe.redirectToCheckout({ sessionId: "cs_test_a1b2c3d4e5f6g7h8i9j0" });
    ```
* Upon successful payment, the user will be redirected to the `success_url`. If canceled, the user will be redirected to the `cancel_url`.


2. **Retrieve Subscription Status**

   **URL:** `/api/subscription-status/`
   **Method:** `GET`
   **Permissions:** Only users with roles `FundAdmin` or `FundManager`.

   **Description:**
   This endpoint retrieves the user's subscription status, including plan name, billing interval (annual or monthly), and next renewal date.

**Response (With Active Subscription):**
```json
{
  "status": "active",
  "current_period_end": 1702892956,
  "plan_name": "Pro Plan",
  "interval": "year"
}
```
* `status`: The current subscription status (e.g., active, canceled, past_due).
* `current_period_end`: Unix timestamp representing the end date of the current billing period.
* `plan_name`: The name of the subscribed plan. If a nickname is not provided in Stripe, the product name is used.
* `interval`: Billing interval for the subscription (year or month).

**Response (No Active Subscription):**
```json
{
  "status": "No active subscription"
}
```

**Response (Error):**
```json
{
  "error": "Stripe API error or invalid customer email."
}
```

**Notes:**
* This endpoint uses the authenticated user's email to retrieve their subscription from `Stripe`.
* Ensure that the user's email is associated with a `Stripe Customer`.
* The `current_period_end` timestamp can be converted to a human-readable date on the client side.


## Frontend

1. Set up project environment

   - Languages: HTML, CSS, and JavaScript.
   - File Structure:
     - Separate CSS files for web (style.css) and mobile (mobile.css) to manage specific styles for different platforms.
     - JavaScript will be used for dynamic interactions and API integration.
     - Maintain a clean and scalable project structure for future development, ensuring easy modification and feature expansion.

2. Website Layout Design (Desktop-First Approach)

   - General Structure:
     - Create a basic structure for the webpage that includes a header, navigation, main content area, and footer.
     - Apply CSS Grid or Flexbox for a responsive and flexible layout.
     - Ensure that the navigation bar is well-styled and intuitive, providing clear paths for users to access different parts of the application.
   - Responsive Design:
     - Initially focus on the desktop layout to ensure the design works well on larger screens.
     - Implement a clean and minimalistic approach with proper spacing, alignment, and structure, making sure it's easy to scale down for mobile screens later.

3. Mobile Layout Design (Mobile-First Approach)

   - Media Queries:
     - Use media queries to design layouts for various screen sizes (e.g., 320px, 480px, 768px). This ensures the site is optimized for both mobile and desktop devices.
     - Focus on smaller screens first and build up, applying different breakpoints for fluid responsiveness.
   - Mobile-Friendly Navigation:
     - Create a hamburger menu or collapsible menu for mobile users. This ensures the navigation bar adapts smoothly to different screen sizes.
     - Optimize interactive areas such as buttons, icons, and touchable links for mobile users. Ensure sufficient spacing for easy interaction, especially on touch devices..

4. Typography and Colour Scheme

   - Typography:
     - Choose font families and sizes that work well across both web and mobile platforms, ensuring readability on all screen sizes.
     - Adjust line spacing and text alignment based on screen size to maintain clean readability across devices.
   - Colour Palette:
     - Define a consistent colour scheme for background, text, buttons, and links. Create separate palettes for both web and mobile to ensure visual consistency across platforms.
     - Ensure that colour choices comply with accessibility standards by testing the contrast ratio and legibility of text against backgrounds, particularly for users with visual impairments.

5. Performance Optimization

   - CSS Optimization:
     - Minify CSS files for both web (style.css) and mobile (mobile.css) to reduce file size and improve page load times.
     - Use browser-specific optimizations by applying vendor prefixes (e.g., -webkit-, -moz-, -o-) to ensure CSS properties work consistently across different browsers.
   - Load Optimization:
     - Implement asynchronous loading for CSS files where applicable to ensure that styles are loaded in a non-blocking manner, enhancing the user experience by reducing render-blocking issues.

6. Cross-Browser Testing and Debugging

   - Browser Testing:
     - Test the website's layout and functionality across all major browsers, including Chrome, Firefox, Safari, and Edge, ensuring that the design and interactions work consistently.
   - Debugging Tools:
     - Use browser-specific developer tools (e.g., Chrome DevTools, Firefox Inspector) to troubleshoot any layout or JavaScript issues.
     - Debug and fix any inconsistencies in the design, such as padding, margin, and alignment issues, across different browsers.

7. Final QA and Adjustments

   - Comprehensive Testing:
     - Perform a final review of the design and functionality across all devices (desktop, mobile, tablet). Use feedback from the team or lecturers to ensure the site performs well in various scenarios.
   - Issue Resolution:
     - Address any remaining visual or performance issues before final deployment.
   - User Experience Optimization:
     - Gather user feedback to improve the overall user experience, ensuring the interface is intuitive, fast, and responsive.

8. Integration with Backend APIs

   - Use JavaScript to integrate with the backend APIs (built using Django) for dynamic content rendering, such as user authentication, stock portfolio management, and real-time data fetching.
   - Ensure seamless communication between the frontend and backend, including error handling for API calls, smooth data flow, and fast response times.

9. AI Data Visualization Integration

   - Plan for the integration of AI-powered stock price predictions into the frontend interface in later stages.
   - Ensure the layout is flexible enough to accommodate charts, tables, or graphs that will visualize stock trends and market predictions based on the AI model.


### CSS

**- General Body Styling**

```CSS
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #ffffff;
    color: #333;
}
```
  
.Font & Colors: Sets a basic font family of Arial, a common sans-serif font, for readability across devices. Background color (#ffffff) and text color (#333) are chosen for a high contrast, enhancing readability.
.Margins & Padding: By setting these to 0, it removes any default spacing, allowing for more control over layout spacing.

**- Header Styling**

```CSS
header {
    background-color: #0073e6;
    padding: 20px;
    text-align: center;
    color: white;
    font-size: 1.8em;
    font-weight: bold;
}
```
  
.Color & Text Styling: The header has a bold blue background (#0073e6) and white text to make it prominent. The large font size and bold styling indicate its importance as a key site element.
.Centering Text: Text is centered for a balanced, visually pleasing look.

**- Navigation Styling**

```CSS
nav {
    background-color: #005bb5;
    overflow: hidden;
    display: flex; /* Ensures items are in a row */
    justify-content: center; /* Centers the navigation items */
}

nav a {
    display: block;
    color: white;
    text-align: center;
    padding: 14px 20px;
    text-decoration: none;
    font-size: 1.2em;
}

nav a:hover {
    background-color: #004494;
    color: #fff;
}


nav ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
}

nav ul li {
    margin-right: 20px;
}

nav ul li:last-child {
    margin-right: 0;
}

nav ul li a {
    color: white;
    text-decoration: none;
    padding: 10px 20px;
    background-color: #005bb5;
    border-radius: 5px;
    font-size: 1.2em;
}

nav ul li a:hover {
    background-color: #004494;
}
```
  
.Responsive Flex Layout: The navigation bar is styled with flex to align items in a row, providing easy access to navigation links. Centering (justify-content: center) ensures that links are balanced and intuitively placed.
.Link Colors & Hover Effects: Links are white on a dark blue background, ensuring readability. The hover effect slightly darkens the background (#004494), providing feedback to users when they interact with a link.
.List Item Styling: nav ul li items are spaced out with margin-right, ensuring sufficient space between links for easy clickability on desktop screens. Last items have no right margin to align with the container’s edge.

**- Main Content Styling**

```CSS
main {
    padding: 20px;
    text-align: center;
}

main h1 {
    color: #0073e6;
    font-size: 2.5em;
    margin-bottom: 10px;
}

main p {
    font-size: 1.1em;
    color: #555;
    margin-bottom: 30px;
}
```
  
.Section Text Centering & Max Width: The main content section uses centered text and a max width (800px) to keep line lengths manageable for reading.
.Headings and Text Colors: Blue (#0073e6) heading colors and light grey text (#666) help distinguish section titles and paragraphs, adding visual hierarchy.
.Image Styling: Section images are set to 50% width, keeping them adaptable to different screen sizes. The rounded corners add a modern, friendly appearance.

**- Form Styling**

```CSS
form {
    max-width: 500px; /* Centering the form */
    margin: 0 auto; /* Centering the form */
    background-color: #fff; /* Form background color */
    border-radius: 8px; /* Rounded corners */
    padding: 20px; /* Padding inside the form */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Box shadow for depth */
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

form label {
    text-align: left;
    color: #333;
    font-weight: bold;
}

form input, form textarea {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
}

form textarea {
    resize: vertical;
    min-height: 100px;
}

form button {
    background-color: #0073e6;
    color: white;
    padding: 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}

form button:hover {
    background-color: #005bb5;
}
```
  
.Centering & Box Shadow: The form is centered and has a box shadow for depth, visually separating it from the rest of the page.
.Form Inputs: Text inputs and text areas are padded and have rounded borders, improving usability and aesthetics.
.Form Button: The button color (#0073e6) matches the overall theme. The hover effect on buttons gives a clear, interactive feel, enhancing user feedback.

**- Footer Styling**

```CSS
footer {
    background-color: #0073e6;
    padding: 10px;
    text-align: center;
    color: white;
    position: fixed;
    width: 100%;
    bottom: 0;
}

footer p {
    margin: 0;
    font-size: 0.9em;
}
```

.Fixed Positioning: The footer is styled to stay at the bottom of the page, with a consistent background color (#0073e6) and white text. It’s small enough to avoid obstructing content but provides easy access to footer information.

**- Button Styling**
```CSS
button, .btn {
    background-color: #005bb5;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
}

button:hover, .btn:hover {
    background-color: #004494;
}
```
  
.Consistent Button Design: All buttons share a similar blue background and white text with rounded borders, giving them a cohesive look. The color change on hover provides feedback, improving interaction experience.

**- Responsive Design**

```CSS
@media (max-width: 768px) {
    nav a {
        float: none;
        width: 100%;
        text-align: left;
    }
}
```

.Mobile Navigation: At widths below 768px, navigation links take up the full width and are aligned to the left for easier tapping on mobile screens. This approach maintains usability across devices.

**- Overall User Friendliness**

.Color and Spacing: Consistent colors across sections enhance brand cohesion. Spacing and padding make elements easily clickable and visually distinct.
.Intuitive Interactivity: Hover effects and clearly defined buttons guide users in navigating the website.
.Responsive Adjustments: Adaptable layouts ensure the design remains accessible and legible on both desktop and mobile, optimizing user experience across all screen sizes.

This code enhances user-friendliness by creating a visually cohesive, responsive design that is easy to navigate and interact with, whether on desktop or mobile.

### Ai
### crewAI - Framework for creating and managing AI agents

crewAI will be used to create and manage AI agents that work together to accomplish complex tasks.

Key Features:
- Agent Creation: Define specialized AI agents for different roles within the trading system
- Task Management: Coordinate tasks between agents for efficient workflow
- Communication: Enable inter-agent communication for collaborative problem-solving
- Integration: Seamlessly integrate with other AI tools and APIs

### Groq API - For fast language model inference

Groq API is utilized for fast inference in time-sensitive trading operations.

Implementation:
- Real-time Analysis: Process market data and news in real-time
- Quick Decision Making: Generate rapid insights for trading strategies
- Low-latency Responses: Ensure timely execution of trades

### OpenAI API - For advanced language model capabilities

- OpenAI API provides advanced language model capabilities for complex analysis and decision-making at fast inference.
- Provides entrypoint for ollama driven local models for integration with langchain & crewAI.

### Integration

- Integrated AI functionalities for stock prediction and historical data analysis.
- APIs like Yahoo Finance and Alpha Vantage are used for real-time and historical market data.


### Docker Integration

The use of ``Docker`` became essential due to the integration of AI functionalities, which significantly increased the complexity of managing dependencies. By containerizing the application, we ensure that all dependencies — especially those related to AI models and libraries—are consistently managed and isolated across different environments.

Managing these dependencies in a local development environment proved to be challenging due to potential conflicts with other libraries and platform-specific issues. Docker resolves these challenges by providing a consistent and isolated environment for the application.

#### Docker Setup

1. Build Docker Images:
```bash
docker-compose build
```

2. Run Containers:
```bash
docker-compose up
```

3. Access Application:
 * Backend: ``http://localhost:8000/``
 * SQLite: Used for system-level data.
 * Firebase Firestore: Configured for business logic.

#### Docker Compose File

This section describes the `docker-compose.yml` file used to set up and run the project backend.

```yaml
version: '3.9'

services:
  web:
    build:
      context: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - ./config/act-corporate-trader-firebase-adminsdk-uwhis-21e99a6344.json:/app/config/firebase_credentials.json
    env_file:
      - .env
    environment:
      - DJANGO_SETTINGS_MODULE=act_backend.settings
      - FIREBASE_CREDENTIALS_FILE=firebase_credentials.json
```

**Explanation of Configuration:**

1. ``version: '3.9'``: Specifies the Docker Compose file format version.

2. ``services:`` Defines the services to be run in the Docker environment.

3. ``web`` service:

    * ``build:``
        * ``context: .`` instructs Docker to use the current directory as the build context.
    * ``ports:``
        * Maps the container's port 8000 to the host's port 8000, enabling access to the Django application at ``http://localhost:8000``.
    * ``volumes:``
        * ``.:/app:`` Mounts the project directory from the host to /app in the container, enabling live code changes without rebuilding the container.
        * ``./config/act-corporate-trader-firebase-adminsdk-uwhis-21e99a6344.json:/app/config/firebase_credentials.json:`` Mounts the Firebase credentials file into the container at the specified path.
    * ``env_file:``
        * Specifies the ``.env`` file to load additional environment variables.
    * ``environment:``
        * ``DJANGO_SETTINGS_MODULE:`` Specifies the Django settings module for the application.
        * ``FIREBASE_CREDENTIALS_FILE:`` Defines the name of the Firebase credentials file within the container.

#### Notes

* ``AI Integration:`` The AI libraries and models are managed within the container, ensuring compatibility across environments and reducing setup complexity.
* ``Firebase Integration:`` Ensure that the Firebase Admin SDK JSON file is correctly placed in the config directory and referenced in the volumes section.
* ``Live Code Changes:`` The volumes directive allows live code changes to reflect without rebuilding the container.
* ``Environment Variables:`` The .env file centralizes environment-specific configuration, making the application portable across different environments.


### Product Backlog
**Please teams, improve this content, it's only sceleton.**

Here's a product backlog by sprint breakdown for the "ACT (Agentic Corporate Trader)" project, aligned with the parallel development of frontend, backend, and AI.

### Sprint 1: Initial Setup and Core Development

| **ID** | **Feature/Task**                                     | **Assigned To**        | **Priority** | **Estimated Effort** | **Notes**                                                 |
|--------|------------------------------------------------------|------------------------|--------------|----------------------|-----------------------------------------------------------|
| 1      | Backend Setup: Initialize Django project             | Backend Developer      | High         | 4 hours               | Start backend API and development             |
| 2      | User Authentication: Implement Allauth               | Backend Developer      | High         | 5 hours               | Setup social login integration (Google/Facebook)           |
| 8      | Frontend Setup: Initialize project structure         | Frontend Developers (2) | High        | 4 hours               | Start frontend development                    |
| 9      | Responsive Design: Create web (desktop) layout       | Frontend Developers (2) | High        | 6 hours               | Basic layout and responsive design for the web version     |
| 12     | AI Integration: Implement AI engine (Phase 1)        | AI Developer            | High        | 6 hours               | Initial setup of AI models and environment                 |
| 16     | Documentation: Prepare README & setup instructions   | Backend Developer      | High         | 2 hours               | Setup documentation          |

### Sprint 2: API Development and Advanced Frontend

| **ID** | **Feature/Task**                                     | **Assigned To**        | **Priority** | **Estimated Effort** | **Notes**                                                 |
|--------|------------------------------------------------------|------------------------|--------------|----------------------|-----------------------------------------------------------|
| 3      | JWT Authentication: Integrate SimpleJWT              | Backend Developer      | High         | 4 hours               | Secure token-based authentication for API                 |
| 4      | API for Stock & Crypto Management: Create REST APIs  | Backend Developer      | High         | 8 hours               | Core API functionality for buying/selling assets           |
| 10     | Mobile Layout Design: Design mobile-first approach   | Frontend Developers (2) | High        | 5 hours               | Responsive design for mobile                              |
| 12     | AI Integration (Phase 2): Develop stock recommendations logic | AI Developer    | High        | 8 hours               | Connect models to analyze stocks/crypto and make recommendations |
| 14     | Cross-Browser Testing: Test on different browsers    | Frontend Developers (2) | Medium      | 3 hours               | Ensure compatibility across browsers                      |

### Sprint 3: Finalize Features and Testing

| **ID** | **Feature/Task**                                     | **Assigned To**        | **Priority** | **Estimated Effort** | **Notes**                                                 |
|--------|------------------------------------------------------|------------------------|--------------|----------------------|-----------------------------------------------------------|
| 5      | Admin Interface: Set up Django admin for fund managers| Backend Developer      | Medium       | 6 hours               | Admin panel for managing users and funds                  |
| 6      | Firebase Integration: Connect Firebase SDK           | Backend Developer      | Medium       | 5 hours               | Sync with Firebase for user data storage                  |
| 7      | Payment Gateway Integration: Add Stripe/PayPal       | Backend Developer      | Medium       | 6 hours               | Payment processing for premium features                   |
| 11     | Typography & Color Scheme: Define styles             | Frontend Developers (2) | Medium       | 4 hours               | Finalize design choices for the web and mobile versions   |
| 13     | Performance Optimization: Minify CSS, JS             | Frontend Developers (2) | Medium       | 3 hours               | Optimize performance for both web and mobile platforms    |
| 15     | Final QA & Adjustments: Review and fix issues        | Entire Team            | High         | 4 hours               | Fix any remaining issues based on testing and feedback    |

### Sprint 4: Final Adjustments and Handoff

| **ID** | **Feature/Task**                                     | **Assigned To**        | **Priority** | **Estimated Effort** | **Notes**                                                 |
|--------|------------------------------------------------------|------------------------|--------------|----------------------|-----------------------------------------------------------|
| 16     | Final Review: Prepare submission for supervisor      | Group Leader           | High         | 2 hours               | Finalize documentation and demonstrate environment         |
| 12     | AI Integration (Finalization): Test AI engine with API| AI Developer           | High         | 4 hours               | Ensure AI is fully functional and integrated with API      |
| 15     | Final QA & Adjustments: Perform final review         | Entire Team            | High         | 4 hours               | Fix last-minute issues and optimize for submission         |


### Summary:

**Total Number of Tasks: 20**

**Total Estimated Hours: 85 hours**

**Sprint Breakdown:**

* **Sprint 1:**

    Number of Tasks: 6
    Total Hours: 27 hours

* **Sprint 2:**

    Number of Tasks: 5
    Total Hours: 28 hours

* **Sprint 3:**

    Number of Tasks: 6
    Total Hours: 28 hours

* **Sprint 4:**

    Number of Tasks: 3
    Total Hours: 10 hours

**Please teams, improve this content, it's only sceleton.**

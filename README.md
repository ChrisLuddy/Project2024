# Project2024
ACT (Agentic Corporate Trader)
# Project Readme File


## Table of contents 
- [Features of the website](#features)
- [Database Configuration](#database-configuration)
- [Data Model Overview](#data-model-overview)
- [Database Diagram](#database-diagram)
- [Backend](#backend)
- [External APIs Integration](#external-apis-integration)
- [Frontend](#frontend)
- [Ai](#ai)
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

### Database-Configuration

In this project, we are using a combination of **SQLite** and **Firebase Firestore** for data management. 

- **SQLite**: Used for Django's built-in system data (e.g., user authentication, admin panel, sessions other system-level data).
- **Firebase Firestore**: Used for storing business logic data (e.g., assets, trades, user portfolios).


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

- **API Endpoints**: The API can be accessed by using the following paths:

  - **User Registration**: 
    ```bash
    POST http://161.35.38.50:8000/api/register/
    ```

  - **JWT Authentication**:
    ```bash
    POST http://161.35.38.50:8000/api/token/
    ```

  - **JWT Token Refresh**:
    ```bash
    POST http://161.35.38.50:8000/api/token/refresh/
    ```

  - **Yahoo Finance API**:
    ```bash
    GET http://161.35.38.50:8000/api/yahoo-finance/
    ```

  - **Alpha Vantage API**:
    ```bash
    GET http://161.35.38.50:8000/api/alpha-vantage/
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

### Work in admin panel

1) ***Creating Fund Administrator or Fund Manager from admin panel***
    You can to add users with the roles **Fund Administrator** and **Fund Manager** through the Django admin interface:

    1. Go to the admin panel at `{{url}}/admin/`.
    2. Log in using your superuser credentials.
    3. Navigate to **CORE > Users** and add new users. You can assign them the roles **Fund Administrator** or **Fund Manager** as needed.
    4. **Ensure** that the **is_staff** and **is_active** flags are checked for the users you create. This allows them to log in and interact with the system.
    5. After creating the users, you can authenticate them via the API.

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
    "username": "admin_user",
    "password": "securepassword123",
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
    "username": "admin_user",
    "password": "securepassword123",
    "role": "fund_admin"
}
```

Example Responses: 

1) Status: 201 Created

```json
{
    "id": 1,
    "username": "admin_user",
    "role": "fund_admin",
    "message": "User registered successfully!"
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
    "username": "username",
    "password": "password"
}
```

This will return access and refresh tokens, which are used to authenticate API requests. 

For example:
```json
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
curl -X GET 'http://127.0.0.1:8000/api/yahoo-finance/?ticker=AAPL&type=STOCKS'
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


#### Alpha Vantage API:

The Alpha Vantage API provides historical and real-time stock data, including daily time series, which shows the open, high, low, close prices, and volume for each day. This is particularly useful for performing technical analysis or retrieving historical trends of a stock.

**URL:** `/api/alpha-vantage/`

**Request Method:** `GET`

**Request Parameters:**
- `symbol`: The stock ticker symbol (e.g., `AAPL` for Apple Inc.).
- `function`: The type of time series data (e.g., TIME_SERIES_DAILY).
- `outputsize`: Data size, either compact (latest 100 data points) or full (all available data).

```bash
curl -X GET 'http://127.0.0.1:8000/api/alpha-vantage/?symbol=AAPL'
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

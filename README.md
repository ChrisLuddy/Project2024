# Project2024
ACT (Agentic Corporate Trader)
# Project Readme File


## Table of contents 
- [Backend](#Backend)
- [Frontend](#Frontend)
- [Ai](#Ai)
- [Product Backlog](#product-backlog)

### Backend

#### Requirements

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

#### Database Configuration

In this project, we are using a combination of **SQLite** and **Firebase Firestore** for data management. 

- **SQLite**: Used for Django's built-in system data (e.g., user authentication, admin panel, sessions other system-level data).
- **Firebase Firestore**: Used for storing business logic data (e.g., assets, trades, user portfolios).

#### Backend Installation Guide

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
9. ***API Authentication***

    The project uses JWT (JSON Web Tokens) for authentication. Before using the API, you need to add users with the roles **Fund Administrator** and **Fund Manager** through the Django admin interface:

    1. Go to the admin panel at `http://127.0.0.1:8000/admin/`.
    2. Log in using your superuser credentials.
    3. Navigate to **CORE > Users** and add new users. You can assign them the roles **Fund Administrator** or **Fund Manager** as needed.
    4. **Ensure** that the **is_staff** and **is_active** flags are checked for the users you create. This allows them to log in and interact with the system.
    5. After creating the users, you can authenticate them via the API.

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

    This will return access and refresh tokens, which are used to authenticate API requests. For example:
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

## Frontend

1.Set up project environment 
- Language: HTML, CSS, and Java.
- Separate CSS files for web (style.css) and mobile (mobile.css) to manage specific styles.
- Clean project structure for future development.
  
2. Website Layout Design (Desktop First Approach)
- Create a general structure for the webpage (header, navigation, main content area, footer).
- Apply grid or flexbox for responsive layout.
- Ensure navigation is styled and easy to use.
  
3. Mobile Layout Design (Mobile First Approach)
-Use media queries to design layouts for different screen sizes (320px, 480px, etc.).
-Design a mobile-friendly navigation menu (hamburger or collapsible).
-Optimize touch areas for mobile interactions (e.g., buttons and links also various screen sizes)

4. Typography and Colour Scheme (colour palettes for both web and mobile) Choose font families, sizes, and line spacing suitable for both platforms.
- Define a colour palette for background, text, buttons, and links.
- Ensure that the colours meet accessibility standards (contrast, legibility).

5.Performance Optimization (code)
- Minify CSS for both web and mobile.
- Use browser-specific optimizations (I will use -webkit-, -moz- prefixes).
- Optimize CSS load times by using asynchronous loading where possible.

6. Cross-Browser Testing and Debugging (Ensure cross-browser compatibility)
- Test your design on different browsers (Chrome, Firefox, Safari, Edge).
- Use developer tools to debug layout issues.
 - Fix any inconsistencies in design across browsers.

7. Final QA and Adjustments
- Conduct a final review of the design across all devices. (ask group, lectures)
- Fix any remaining visual or performance issues.
- Optimize the overall user experience by gathering feedback.




## Ai
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


## Product Backlog
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

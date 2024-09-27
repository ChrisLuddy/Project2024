# Project2024
ACT (Agentic Corporate Trader)
# Project Readme File


## Table of contents 
- [Technologies](#Technologies)
- [Backend](#Backend)
- [Frontend](#Frontend)
- [Ai](#Ai)

## Technologies

### Backend

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

**Login-Signup-Page**

This project is a backend authentication system built using a lightweight Python framework such as Flask. 
It demonstrates how modern authentication systems work using JWT (JSON Web Tokens) and a simple SQLite database.

**Technologies Used**

Frontend: HTML5, CSS3 (Bootstrap + custom styling),JavaScript.
Backend: Python Flask Framework, Flask-JWT-Extended (Authentication).
Database: SQLite3, SQLAlchemy ORM.
Security: Werkzeug (Password hashing), JWT Token Authentication.

**1. User Registration (Signup)**
Users can create a new account,
Password is securely hashed before storing in database
Prevents duplicate usernames.

**3. User Login**
Users can log in using username and password,
JWT token is generated after successful login,
Token is used for secure authentication.

**4. User Profile View**
Displays user details from database,
Accessible only after successful login,
Protected using JWT authentication.

**6. Update Profile**
Users can update their profile details,
Changes are saved in SQLite database,
Requires authentication token.

**8. Logout Functionality**
Clears stored token and user session,
Redirects user to login page.

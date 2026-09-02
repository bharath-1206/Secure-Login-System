# 🔐 Secure Login System

A simple secure login web application built with Python and Flask.

The project demonstrates basic web application security concepts including password hashing, input validation, SQL injection protection, authentication, and session management.

## ✨ Features

- User registration
- Secure password hashing using bcrypt
- Password validation
- Email and username validation
- Protection against SQL injection using parameterized queries
- User authentication
- Session management
- Secure logout
- Basic security headers
- Simple responsive interface

## 🛠️ Technologies

- Python
- Flask
- SQLite
- bcrypt
- HTML
- CSS

## 🔐 Security

### Password Hashing

User passwords are never stored as plain text.

Passwords are hashed using the bcrypt algorithm before being stored in the database.

### SQL Injection Protection

Database queries use parameterized SQL statements instead of directly inserting user input into SQL queries.

### Input Validation

The application validates:

- Username format
- Email format
- Password length
- Password complexity

### Session Management

Authenticated users receive a server-side session.

The session is cleared when the user logs out.

### Security Headers

The application includes basic security headers such as:

- `X-Content-Type-Options`
- `X-Frame-Options`
- `Referrer-Policy`

## 📁 Project Structure

```text
Secure-Login-System/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── templates/
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
│
└── static/
    └── style.css

⚙️ Installation

Clone the repository:
git clone https://github.com/bharath-1206/Secure-Login-System.git

Move into the project directory:
cd Secure-Login-System

Install the dependencies:
pip install -r requirements.txt

Run the application:
python app.py

The application will be available at:
http://127.0.0.1:5000
🧪 Security Testing

The application can be tested using:

Registration
Create an account using a valid username, email and password.
Login
Log in using the registered credentials.
Invalid Login
Try an incorrect password and verify that access is denied.
SQL Injection Test

Try entering a basic SQL injection payload such as:
' OR '1'='1
The application should not bypass authentication because it uses parameterized SQL queries.
Logout
Log out and try accessing the dashboard again.
The application should redirect the user back to the login page.

⚠️ Limitations
This is an educational security project and is not intended to be used as a production authentication system.
For a production application, additional protections should be implemented, including:
CSRF protection
Rate limiting
Account lockout controls
Multi-factor authentication
Secure HTTPS deployment
Stronger password policies
Password reset security
Security monitoring and logging

🚀 Future Improvements
Add Two-Factor Authentication (2FA)
Add CSRF protection
Add login rate limiting
Add password reset functionality
Add account lockout after repeated failures
Add email verification
Deploy using HTTPS

🧠 What I Learned
This project helped me understand how authentication systems should handle passwords, user input, database queries and sessions securely.
It also gave me practical experience with:
Password hashing
Authentication
Session management
SQL injection prevention
Input validation
Flask web development
Secure coding practices

👨‍💻 Author
Bharath M
Cybersecurity Engineering Student

GitHub:
https://github.com/bharath-1206/Secure-Login-System

📌 Disclaimer
This project is created for educational and authorized security-testing purposes.

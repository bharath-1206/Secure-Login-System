import os
import re
import secrets
import sqlite3

import bcrypt

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)


app = Flask(__name__)

# Use an environment variable in real deployments.
# A random key is generated for local development.
app.secret_key = os.environ.get(
    "SECRET_KEY",
    secrets.token_hex(32)
)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

DATABASE = "users.db"


def get_db():
    """Create and return a SQLite database connection."""

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    """Create the users table if it does not exist."""

    connection = get_db()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def valid_email(email):
    """Perform basic email validation."""

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(pattern, email) is not None


def valid_username(username):
    """Allow letters, numbers and underscores."""

    return re.fullmatch(
        r"[A-Za-z0-9_]{3,20}",
        username
    ) is not None


def valid_password(password):
    """Check basic password security requirements."""

    return (
        len(password) >= 8
        and any(char.isupper() for char in password)
        and any(char.islower() for char in password)
        and any(char.isdigit() for char in password)
    )


@app.after_request
def add_security_headers(response):
    """Add basic browser security headers."""

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response


@app.route("/")
def home():
    """Redirect users to the appropriate page."""

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        if not valid_username(username):

            flash(
                "Username must contain 3-20 letters, numbers or underscores.",
                "error"
            )

            return render_template("register.html")

        if not valid_email(email):

            flash(
                "Please enter a valid email address.",
                "error"
            )

            return render_template("register.html")

        if not valid_password(password):

            flash(
                "Password must contain at least 8 characters, including uppercase, lowercase and a number.",
                "error"
            )

            return render_template("register.html")

        connection = get_db()

        existing_user = connection.execute(
            """
            SELECT id
            FROM users
            WHERE username = ? OR email = ?
            """,
            (username, email)
        ).fetchone()

        if existing_user:

            connection.close()

            flash(
                "Username or email is already registered.",
                "error"
            )

            return render_template("register.html")

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        connection.execute(
            """
            INSERT INTO users (
                username,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                username,
                email,
                password_hash
            )
        )

        connection.commit()
        connection.close()

        flash(
            "Registration successful. You can now log in.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        connection = get_db()

        user = connection.execute(
            """
            SELECT id, username, password_hash
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        connection.close()

        if user and bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        ):

            session.clear()

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid username or password.",
            "error"
        )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        flash(
            "Please log in to continue.",
            "error"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


@app.route("/logout", methods=["POST"])
def logout():

    session.clear()

    flash(
        "You have been logged out successfully.",
        "success"
    )

    return redirect(
        url_for("login")
    )


if __name__ == "__main__":

    init_db()

    app.run(
        debug=True
      )

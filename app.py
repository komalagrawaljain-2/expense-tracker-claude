from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email

app = Flask(__name__)
app.secret_key = "dev-secret-change-in-prod"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not name or not email or not password:
            return render_template("register.html", error="All fields are required.", name=name, email=email)
        if len(password) < 8:
            return render_template("register.html", error="Password must be at least 8 characters.", name=name, email=email)

        password_hash = generate_password_hash(password)
        try:
            user_id = create_user(name, email, password_hash)
        except sqlite3.IntegrityError:
            return render_template("register.html", error="An account with that email already exists.", name=name, email=email)

        session["user_id"] = user_id
        session["user_name"] = name
        return redirect(url_for("landing"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            return render_template("login.html", error="All fields are required.")

        user = get_user_by_email(email)
        if user is None or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="Invalid email or password.")

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("profile"))

    return render_template("login.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
@login_required
def profile():
    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "2026-01-15",
        "initials": "DU",
    }

    stats = {
        "total_spent": 351.24,
        "transaction_count": 8,
        "top_category": "Food",
    }

    transactions = [
        {"date": "2026-05-15", "description": "Coffee and snacks",  "category": "Food",          "amount": 8.75},
        {"date": "2026-05-13", "description": "Miscellaneous",      "category": "Other",         "amount": 15.00},
        {"date": "2026-05-11", "description": "Clothing",           "category": "Shopping",      "amount": 89.99},
        {"date": "2026-05-09", "description": "Movie tickets",      "category": "Entertainment", "amount": 25.00},
        {"date": "2026-05-07", "description": "Pharmacy",           "category": "Health",        "amount": 35.00},
        {"date": "2026-05-05", "description": "Electricity bill",   "category": "Bills",         "amount": 120.00},
        {"date": "2026-05-03", "description": "Monthly bus pass",   "category": "Transport",     "amount": 45.00},
        {"date": "2026-05-01", "description": "Lunch at cafe",      "category": "Food",          "amount": 12.50},
    ]

    categories = [
        {"name": "Bills",         "total": 120.00, "pct": 34},
        {"name": "Shopping",      "total": 89.99,  "pct": 26},
        {"name": "Transport",     "total": 45.00,  "pct": 13},
        {"name": "Health",        "total": 35.00,  "pct": 10},
        {"name": "Entertainment", "total": 25.00,  "pct": 7},
        {"name": "Food",          "total": 21.25,  "pct": 6},
        {"name": "Other",         "total": 15.00,  "pct": 4},
    ]

    return render_template("profile.html",
                           user=user,
                           stats=stats,
                           transactions=transactions,
                           categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)

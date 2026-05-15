# Spec: Registration

## Overview
Implement user registration so new visitors can create a Spendly account. This step wires up the existing `register.html` form to a POST handler that validates input, hashes the password, inserts the user into the database, starts a session, and redirects to the landing page. It also adds Flask session support (secret key) which all authenticated features depend on.

## Depends on
- Step 01 — Database Setup (users table must exist)

## Routes
- `GET /register` — render registration form — public
- `POST /register` — handle form submission, create user, start session, redirect — public

## Database changes
No new tables or columns. A new helper function is needed in `database/db.py`:
- `create_user(name, email, password_hash)` — inserts a row into `users`, returns the new `id`. Raises `sqlite3.IntegrityError` on duplicate email.

## Templates
- **Create:** none
- **Modify:**
  - `templates/register.html` — already exists and is complete; no changes needed if the route passes `error` correctly
  - `templates/base.html` — update nav links to show username / logout when a session exists, and Sign in / Get started when not logged in

## Files to change
- `app.py` — add `app.secret_key`, convert `/register` to accept GET and POST, import session from flask, import `create_user` from `database.db`
- `database/db.py` — add `create_user()` function

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with `werkzeug.security.generate_password_hash` before storing
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `app.secret_key` must be set before any session use; use a hard-coded dev string (e.g. `"dev-secret-change-in-prod"`) — no env file needed at this stage
- On duplicate email, catch `sqlite3.IntegrityError` and re-render the form with `error="An account with that email already exists."`
- On success, store `session['user_id']` and `session['user_name']`, then redirect to `url_for('landing')`
- Validate server-side: name and email and password must not be empty; password must be at least 8 characters — render form with an `error` message if invalid

## Definition of done
- [ ] Visiting `/register` renders the registration form
- [ ] Submitting with valid name, email, and password (8+ chars) creates a new row in the `users` table with a hashed password
- [ ] After successful registration the browser redirects to the landing page (`/`)
- [ ] `session['user_id']` is set after registration
- [ ] Submitting with a duplicate email re-renders the form with an error message (no crash)
- [ ] Submitting with a password shorter than 8 characters re-renders the form with an error message
- [ ] Submitting with any empty field re-renders the form with an error message
- [ ] The nav in `base.html` shows the logged-in user's name (or a logout link) when a session exists

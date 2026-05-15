# Spec: Login and Logout

## Overview
Implement login and logout so registered users can authenticate into Spendly and end their session. The login form accepts email and password, verifies the credentials against the database using `check_password_hash`, sets the session, and redirects to the landing page. The logout route clears the session and redirects to the landing page. This step gates the rest of the app behind authentication and is a prerequisite for all logged-in features.

## Depends on
- Step 01 — Database Setup (users table must exist)
- Step 02 — Registration (users must be able to exist in the database; session keys established)

## Routes
- `GET /login` — render login form — public
- `POST /login` — validate credentials, start session, redirect — public
- `GET /logout` — clear session, redirect to landing — public

## Database changes
No new tables or columns. A new helper function is needed in `database/db.py`:
- `get_user_by_email(email)` — queries the `users` table for a row matching the given email, returns the row as a `sqlite3.Row` or `None`.

## Templates
- **Create:**
  - `templates/login.html` — login form with email and password fields, error display, and a link to `/register`
- **Modify:**
  - `templates/base.html` — nav should show "Logout" link when `session['user_id']` is set, and "Login" / "Get started" links when not. (May already be partially done from Step 02 — verify and complete if needed.)

## Files to change
- `app.py` — convert `/login` stub to accept GET and POST; implement `/logout` to clear session and redirect; import `check_password_hash` from `werkzeug.security`; import `get_user_by_email` from `database.db`
- `database/db.py` — add `get_user_by_email(email)` function

## Files to create
- `templates/login.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords verified with `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- On invalid credentials (email not found OR password wrong), show the same generic error: `"Invalid email or password."` — never reveal which field was wrong
- On success, store `session['user_id']` and `session['user_name']`, then redirect to `url_for('landing')`
- Logout must call `session.clear()` then redirect to `url_for('landing')`
- Validate server-side: email and password fields must not be empty

## Definition of done
- [ ] Visiting `/login` renders the login form
- [ ] Submitting with a valid email and correct password starts a session and redirects to `/`
- [ ] `session['user_id']` and `session['user_name']` are set after successful login
- [ ] Submitting with an unknown email re-renders the form with `"Invalid email or password."` (no crash)
- [ ] Submitting with a wrong password re-renders the form with `"Invalid email or password."` (no crash)
- [ ] Submitting with any empty field re-renders the form with an error message
- [ ] Visiting `/logout` clears the session and redirects to `/`
- [ ] After logout, the nav no longer shows the user's name
- [ ] The nav in `base.html` shows a "Logout" link when logged in and "Login" / "Get started" links when logged out

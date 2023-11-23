from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helperFunctions import login_required

# Configure application
app = Flask(__name__)

# Configure session to use signed cookies
app.config["SECRET_KEY"] = 'HJlsNj3FaKBndhIiyrJVk7q7D9LLBzaL'
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///gitQuizzes.db")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Register user"""
    if request.method == "POST":
        # get user informations
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # ensure all fields was submitted
        if not username or not email or not password or not confirmation:
            flash("must fill all the field")
            return redirect('/signup')

        # ensure password is matching the confirmation
        if password != confirmation:
            flash("password and confirmation don't match")
            return redirect('/signup')

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ? OR email = ?", username, email)

        # ensure username is unique
        if len(rows) != 0:
            flash("username already exists")
            return redirect('/signup')

        # hash the username's password
        hashed_password = generate_password_hash(password)

        # insert the username into the database
        db.execute(
            "INSERT INTO users (username, email, hash) VALUES(?, ?, ?)", username, email, hashed_password
        )

        # remember which user has registered
        usernames = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = usernames[0]["id"]

        # Redirect user to home page
        return redirect("/dashboard")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('signup.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # get user informations
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Ensure username was submitted
        if not username:
            flash("must provide username")
            return redirect("/login")

        # Ensure password was submitted
        elif not password:
            flash("must provide password")
            return redirect("/login")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], password
        ):
            flash("invalid username and/or password")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/dashboard")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route('/dashboard')
@login_required
def dashboard():
    userinfo = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    return render_template('dashboard.html', userinfo=userinfo)


@app.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)


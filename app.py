import os
import requests

from flask import Flask, flash, url_for, abort, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from authlib.integrations.flask_client import OAuth
from helperFunctions import login_required, getQuestions

# Configure application
app = Flask(__name__)

# Configure session to use signed cookies
app.config["SECRET_KEY"] = 'c6607322-a125-435b-8336-4b480e91eace'
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///gitquizzesdb.db")

# google oauth config
appConf = {
    "OAUTH2_CLIENT_ID": os.getenv("client_id"),
    "OAUTH2_CLIENT_SECRET": os.getenv("client_secret"),
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": "a2e8dfba-366f-445c-bae8-74613313b446",
    "FLASK_PORT": 5000
}

app.secret_key = appConf.get("FLASK_SECRET")
oauth = OAuth(app)

# list of google scopes - https://developers.google.com/identity/protocols/oauth2/scopes
oauth.register(
    "myApp",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f'{appConf.get("OAUTH2_META_URL")}'
)

@app.route('/')
def index():
    if "user_id" in session:
        return redirect('/dashboard')
    else:
        return render_template('index.html')


@app.route("/signin-google")
def googleCallback():
    # fetch access token and id token using authorization code
    token = oauth.myApp.authorize_access_token()

    # Retrieve user_id from the session
    user_info = token.get("userinfo", {})

    # make sure user infos are well formatted
    empty = ""
    name = empty.join(user_info.get("name"))
    email = empty.join(user_info.get("email"))
    picture = user_info.get("picture")

    # query database for username
    rows = db.execute("SELECT * FROM users WHERE username = ? OR email = ?", name, email)

    # if the user is already inserted in database
    if len(rows) != 0:
        session["user_id"] = rows[0]["id"]
        return redirect('/dashboard')
    # else
    else:
        # insert the username into the database
        db.execute(
            "INSERT INTO users (username, email, image) VALUES(?, ?, ?)",
            name,
            email,
            picture
        )

        # remember which user has registered
        username = db.execute("SELECT * FROM users WHERE username = ? AND email = ?", name, email)
        session["user_id"] = username[0]["id"]

        #redirect user to dashboard
        return redirect('/dashboard')


@app.route("/google-login")
def googleLogin():
    if "user_id" in session:
        abort(404)
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))


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
            "INSERT INTO users (username, email, hash, image) VALUES(?, ?, ?, ?)", 
            username, 
            email, 
            hashed_password,
            '/static/img/default-users.jpg'
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
    
    return render_template('dashboard.html', userinfo=userinfo[0])


@app.route('/quiz', methods=["GET", "POST"])
@login_required
def quiz():

    categories = [{'name':'Books', 'id': 10}, {'name': 'Conputers', 'id': 7},{'name': 'History', 'id': 8},{'name': 'Geography', 'id': 9},{'name': 'Mathematics', 'id': 10},{'name': 'Sports', 'id': 11}] 
    data = []
    correct_answers = ['allo', 'malo']

    score = 4
    # correct = 0
    # incorrect = 0
    
    if request.method == "POST":
        
        # Check which form was submitted based on the form name or any other identifier
        if 'form1_submit' in request.form:
            # Get user informations
            category = request.form.get("category")
            difficulty = request.form.get("difficulty")

            if not category or not difficulty:
                flash("You must choose category and difficulty please!")
                return redirect("/quiz") 
            # Get a question, depending on the category/difficulty chosen by the user
            data = getQuestions(category, difficulty)

            return render_template('quiz.html', categories=categories, data=data, category=category, quiz_display='block')

        elif 'form2_submit' in request.form:
            
            for question in data:
                answer = f'qus{question["id"]}'
                if request.form.get(answer) == question["correct_answer"]:
                    score += 1

            return render_template('quiz.html', categories=categories, correct_answers=correct_answers, score=score, quiz_display='none')
    else:
        return render_template('quiz.html', categories=categories, quiz_display='none')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)


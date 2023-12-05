import os

from flask import Flask, flash, url_for, abort, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from authlib.integrations.flask_client import OAuth
from helperFunctions import login_required, getQuestions, is_valid_image_url

# Configure application
app = Flask(__name__, static_url_path='/static')

# Configure session to use signed cookies
app.config["SECRET_KEY"] = 'c6607322-a125-435b-8336-4b480e91eace'
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///gitquizzes.db")

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

# supported gategories
categories = [{'name':'Books', 'id': 10}, {'name': 'Computers', 'id': 18},{'name': 'History', 'id': 23},{'name': 'Geography', 'id': 22},{'name': 'Mathematics', 'id': 19},{'name': 'Sports', 'id': 21}]

@app.route('/')
def index():
    # if there is a user render the dashboard
    if "user_id" in session:
        return redirect('/dashboard')
    # else render the home page
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
    rows = db.execute("SELECT * FROM users WHERE email = ?", email)

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
        
        # pull the new user infos from database
        username = db.execute("SELECT * FROM users WHERE username = ? AND email = ?", name, email)
        
        # insert categories and scores for new user
        for category in categories:
            db.execute(
                "INSERT INTO categories_score (user_id, category_name) VALUES(?, ?)",
                username[0]["id"],
                category['name']
            )
        
        # insert number of correct/incorrect answer for new user
        db.execute(
            "INSERT INTO user_answers_statistics (user_id) VALUES(?)",username[0]["id"])
        
        # remember which user has registered
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

        # pull the new user infos from database
        username = db.execute("SELECT * FROM users WHERE username = ? AND email = ?", username, email)
        
        # insert categories and scores for new user
        for category in categories:
            db.execute(
                "INSERT INTO categories_score (user_id, category_name) VALUES(?, ?)",
                username[0]["id"],
                category['name']
            )
        
        # insert number of correct/incorrect answer for new user
        db.execute(
            "INSERT INTO user_answers_statistics (user_id) VALUES(?)",username[0]["id"])
        
        # remember which user has registered
        session["user_id"] = username[0]["id"]

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

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
    """User Dashboard"""
    
    # get user's personal informations
    userinfo = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    
    # get user's correct answers and incorrect answers
    answer_statistics = db.execute("SELECT * from user_answers_statistics WHERE user_id = ?", session["user_id"])
    
    # get categories score
    user_categories_score = db.execute("SELECT * FROM categories_score WHERE user_id = ?", session["user_id"])
    
    # get the ranks of the users
    ranks = db.execute("SELECT * FROM users ORDER BY overall_score DESC LIMIT 10")
    
    # get the user's history
    user_history = db.execute("SELECT * FROM user_history WHERE user_id = ?", session["user_id"])
    
    
    # render the propre html with all of above data
    return render_template('dashboard.html', userinfo=userinfo[0], answer_statistics=answer_statistics[0], user_categories_score=user_categories_score, ranks=ranks, user_history=user_history)


@app.route('/quiz', methods=["GET", "POST"])
@login_required
def quiz(): 
    """Handle quiz page"""
    
    # handle post methods for quiz page
    if request.method == "POST":

        data, user_answers= [], []
        score = 0
        
        # if submit the first form
        if 'form1_submit' in request.form:
            
            # get user informations
            category_id = request.form.get("category")
            difficulty = request.form.get("difficulty")

            # check user input
            if not category_id or not difficulty:
                flash("You must choose category and difficulty please!")
                return redirect("/quiz") 

            # get a question, depending on the category/difficulty chosen by the user
            data = getQuestions(category_id, difficulty)

            # make sure temp_answers and temp_category_type tables are empty before we insert new data
            # get correct answers table and category type table
            correct_answers = db.execute('SELECT answer FROM temp_answers')
            category_type = db.execute('SELECT * FROM temp_category_type')
            
            # ensure correct answers table is empty
            if len(correct_answers) != 0:
                #  clear correct answers from database
                db.execute("DELETE FROM temp_answers")
            
            # ensure category type table is empty
            if len(category_type) != 0:
                #  clear correct answers from database
                db.execute("DELETE FROM temp_category_type")
            
            # store correct answers
            for question in data:
                db.execute("INSERT INTO temp_answers (answer) VALUES(?)", question["correct_answer"])
            
            # convert category variable type so we can find the name of category chosen by user
            converted_category_id = int(category_id)
            
            # find category chosen by user
            category_name = next((category for category in categories if category['id'] == converted_category_id), None)

            # store category and difficulty
            db.execute("INSERT INTO  temp_category_type (category, difficulty) VALUES(?, ?)", category_name['name'], difficulty)

            # render propre HTML for quiz page
            return render_template('quiz.html', categories=categories, data=data, category_name=category_name['name'], quiz_display='block')
        
        # if submit the second form
        elif 'form2_submit' in request.form:

            # get correct answers
            correct_answers = db.execute('SELECT answer FROM temp_answers')

            # get category type
            category_type = db.execute('SELECT * FROM temp_category_type')

            # colect and store user's answers
            for n in range(1,11):
                id = f'qus{n}'
                if request.form.get(id):
                    user_answers.append(request.form.get(id))
                else:
                    flash("Make sure you answer all the questions before you submit! - Try Again")
                    return redirect('/quiz')
            
            # compare user's answer with correct answers
            for n in range(10):
                # if correct then score++
                if user_answers[n] == correct_answers[n]["answer"]:
                    score += 1
            
            # update categories score table with new score of the specific category the user choose
            # get the current score
            current_score_attempts = db.execute("SELECT * FROM categories_score WHERE user_id = ? AND category_name = ?",
                session["user_id"],
                category_type[0]["category"]
            )

            # chaeck if the category has been taken for the first time from the current user
            if current_score_attempts[0]["attempts"] == 0:
                category_score = score,
            else:
                category_score = (score + current_score_attempts[0]["avg_score"]) / 2

            # update category with new avg score
            db.execute("UPDATE categories_score SET attempts = attempts + ?, avg_score = ? WHERE user_id = ? AND category_name = ?",
                1,
                category_score,
                session["user_id"],
                category_type[0]["category"]
            )
            
            # update user's answers statistics table with new data after user finish quiz
            db.execute("UPDATE user_answers_statistics SET correct_answers = correct_answers + ?, incorrect_answers = incorrect_answers + ? WHERE user_id = ? ",
                score,
                10 - score,
                session["user_id"]
            )
            
            # insert into user's history table data that describe the process
            db.execute("INSERT INTO user_history (user_id, category_name, score, difficulty) VALUES(?, ?, ?, ?)",
                session["user_id"],
                category_type[0]["category"],
                score,
                category_type[0]["difficulty"]
            )

            # finaly update the overall score
            # need to get first the avg score of all category with value greate than 0.0
            avg_score_categories = db.execute("SELECT * FROM categories_score WHERE user_id = ? AND attempts > 0",
                session["user_id"]
            )

            # this is the number that we will divided the sum of all categories greater than 0.0
            categories_length = len(avg_score_categories)
            
            # initialize the sum of categories
            categories_sum = 0

            # calculate sum of categories
            for row in avg_score_categories:
                categories_sum += row["avg_score"]

            # calculate overall score
            overall_score = categories_sum / categories_length

            # update the over all score of the user
            db.execute("UPDATE users SET overall_score = ? WHERE id = ?",
                overall_score,
                session["user_id"]
            )
            
            #  clear correct answers from database
            db.execute("DELETE FROM temp_answers")
            
            #  clear category type from database
            db.execute("DELETE FROM temp_category_type")
            
            # render propre HTML for quiz page
            flash(f"Congratulations! You pass the quiz and this is your score for today: {score} in category: {category_type[0]["category"]}")
            return redirect('/dashboard')
    else:
        return render_template('quiz.html', categories=categories, quiz_display='none')


@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    """Edit your personal informations"""

    # get current user infos
    userinfo = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    answer_statistics = db.execute("SELECT * from user_answers_statistics WHERE user_id = ?", session["user_id"])
    user_history = db.execute("SELECT * FROM user_history WHERE user_id = ?", session["user_id"])
    
    # user reached route via POST
    if request.method == "POST":
        # user inputs
        new_username = request.form.get("new_username")
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_new_password = request.form.get("confirm_new_password")
        new_image = request.form.get("image_link")

        # update username
        if new_username:
            # query database for username
            rows = db.execute("SELECT * FROM users WHERE username = ?", new_username)

            # ensure username doesn't already exists
            if len(rows) != 0:
                flash("username already exists")
                return redirect('/profile')

            # update the user's username then
            db.execute(
                "UPDATE users SET username = ? WHERE id = ?",
                new_username,
                session["user_id"],
            )

            # redirect the user to the updated user profile
            flash("username updated successfully")
            return redirect('/profile')

        # update user's password
        if old_password and new_password and confirm_new_password:
            # query database for username
            rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

            # ensure old password is correct
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"], old_password):
                flash("old password is not correct")
                return redirect('/profile')

            # ensure new password is matching the confirmation
            if new_password != confirm_new_password:
                flash("new password is not matching the confirmation")
                return redirect('/profile')

            # hash the username's new password
            hashed_password = generate_password_hash(new_password)

            # update the user's password
            db.execute(
                "UPDATE users SET hash = ? WHERE id = ?",
                hashed_password,
                session["user_id"],
            )

            # redirect the user to the updated user profile
            flash("You have set new password successfully")
            return redirect('/profile')

        # update user's picture
        if new_image:
        
            # update the user's profile picture
            result, message = is_valid_image_url(new_image)

            if result:
                # Store the image URL in the database or perform other actions
                db.execute("UPDATE users SET image = ? WHERE id = ?",
                    new_image,
                    session["user_id"]
                )
                
                # redirect the user to the updated user profile
                flash('Profile picture updated successfully!')
                return redirect('/profile')
            
            else:
                flash(f'Invalid image. {message}')
                return redirect('/profile')
            

        # make sure at least one important field (fields) is (are) not empty
        if (
            not new_username
            and not old_password
            and not new_password
            and not confirm_new_password
            and not new_image
        ):
            flash("Invalid request: you tried to submit a completely empty form")
            return redirect('/profile')
    
    # user reached route via GET
    else:
        # render user's profile
        return render_template('profile.html', userinfo=userinfo[0], answer_statistics=answer_statistics[0], user_history= user_history)



if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup-in')
def signup():
    return render_template('signup-in.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
# Git-Quizzes

### bref description: 

CS50 - Introduction to Computer Science - Final Project- Full Stack Web App That Provides Daily Challenges (quizzes) - HTML / TailwindCSS / JavaScript / Flask / SQLite3

#### Video Demo: [URL HERE]

## Description:

Welcome to Git-Quizzes! This project was created for the purpose of helping people to build the habit of self improvement every day, by doing certain task every day, and these tasks are about answering questions for a variety of categories that we provide for you (history, sports, computers,...etc.), and you can choose to start with whatever category you want. By engaging with quizzes consistently, users may expand their knowledge base in diverse subjects, fostering a culture of lifelong learning. And if they register, they can track their quiz performance, view their scores over time, track daily tasks in various categories over the year. This feature provides a sense of accomplishment and motivation for users to continue participating in quizzes, aiming to improve their scores and achieve higher ranks.

## Project Files:

### `app.py`

- Description:
    - This file serves as the main entry point for my Flask web application, and handle the logic for every route in it, so every web page of my web application rendered properly with the right data and right user interface.
- Purpose:
    - Initializes the Flask application instance.
    - Defines routes, views, and handles HTTP requests.
    - Connects to the database.
    - handle the google Oauth.
    - Configures and sets up various Flask extensions.
- Design Choices: 
    - In fact, in this file, I followed the workflow when I was creating the finance project in the last problem set of the CS50 course.

### `config.py`

- Description: This file is for load the dotenv extension and make use of it.
- Purpose: Store the environment variables like secret keys etc.

### `helperFunctions.py`

- Description: This file contain helper functions that i am using in my app.py file, like function for decorate routes to require login etc.
- Purpose: 
    - Decorate routes to require login.
    - Get question data from trevia endpoint api.
    - validate images.
- Design Choices: I followed the way you implement the helperFunctions.py in the finance problem set.

### `tailwind.config.js`

- Description: This file contain the configuiration of my tailwind css style.
- Purpose: 
    - Define themes.
    - Define variables for your colors, fonts, ...etc.
    - Add plugins.

### `static/app.js`

- Description: This file contain the whole javaScript that i am using in my website.
- Purpose: 
    - The Toggle button for the mobile navbar.
    - The Heap map chart for tracking user's daily activities/tasks.

### `static/css/main.css`

- Description: This file contain the whole style attributs that is coming from tailwindcss framework that you can use in your html.
- Purpose: 
    - Style your html fast.
    - Easy and simple.

### `static/src/input.css`

- Description: This file contain the css that is added in additional of the tailwind framework.
- Purpose: 
    - Add css style to style your html.

### `templates/homeLayout.html`

- Description: This file contain the layout html of the index.html, signup.html and login.html.
- Purpose: 
    - Help me make my code more compact and reusable using jinjaTemplate.

### `templates/layout.html`

- Description: This file contain the layout html of the dashboard.html, quiz.html and profile.html.
- Purpose: 
    - Help me make my code more compact and reusable using jinjaTemplate.

### `templates/index.html`

- Description: This is the home page of my website.
- Purpose: 
    - Present the website.
    - The purpose of the website.
    - The features of the website.
    - How to use the platform.
    - Answer user's questions about the platform.

### `templates/singup.html` and `templates/login.html`

- Description: Those are the pages responsible of user authentication.
- Purpose: 
    - Make the authentication simpole witth Google oauth.
    - If the user don't have google account, stiil can create account with username and email and password with ease.
    - Give the user the ability to enjoy the platform without limitations.

### `templates/dashboard.html`

- Description: This page contain the html that render all the statistic of the user and also the activities over the year, with friendly, clean and minimal user interface.
- Purpose: 
    - Provide user realtime data.
    - Provide user his statistics so he can know his progress and scores.

### `templates/quiz.html`

- Description: This page is resposible for setuping the questions of the category and difficulty that the user choose and also provide him the ability to answer those questions.
- Purpose: 
    - Give user possibility to choose the type of questions he want.
    - Load questions based on user choices
    - Give the user ability to answer those question with ease.

### `templates/profile.html`

- Description: 
    This page contain the user's informations and some of his statistics and also the dailty tasks tracker, and last but not least inputs to change user's information like username, password and profile picture.
- Purpose: 
    - User can change his personal informations.

## Additional Notes:

- This project still in it's early version, there is a window to add more features in the future, that's why i built this project in a way that make it scalable and maintainable with ease.
- dependencies or external libraries used in this project: 
    - From Python I used: requests, random
    - From flask I used: Flask, flash, url_for, abort, redirect, render_template, request, session, jsonify
    - From cs50 I used:  SQL
    - From flask_session I used: Session
    - From werkzeug.security I used: check_password_hash, generate_password_hash
    - From authlib.integrations.flask_client I used: OAuth
    - From functools I used: wraps
    - from PIL I used: Image
    - from io I used: BytesIO

## And This Was CS50 - 🫡👌



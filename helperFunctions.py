from flask import redirect, session, jsonify
from functools import wraps
import requests
import random

def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def getQuestions(category, difficulty):
    """
    Get question data from trevia endpoint api.
    
    """

    questions_data = []
    url =f"https://opentdb.com/api.php?amount=10&category={category}&difficulty={difficulty}&type=multiple"
    
    try:
        # Make a GET request to the trivia API
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            questions = response.json()["results"]

            # Return the questions as JSON
            for question in questions:
                question.pop("type", None)
                question.pop("difficulty", None)
                question.pop("category", None)
                question["incorrect_answers"].append(question["correct_answer"])
                random.shuffle(question["incorrect_answers"])
                
                questions_data.append(question)
            
            return questions_data

        # If the request was not successful, return an error message
        return jsonify({'error': 'Failed to fetch questions'}), response.status_code

    except Exception as error:
        # Handle exceptions, such as connection errors
        return jsonify({'error': str(error)}), 500

    
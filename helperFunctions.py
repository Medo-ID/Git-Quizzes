from flask import redirect, session, jsonify
from functools import wraps
import requests
import random
from PIL import Image
from io import BytesIO

def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def getQuestions(category_id, difficulty):
    """Get question data from trevia endpoint api."""
    number = 1
    questions_data = []
    url =f"https://opentdb.com/api.php?amount=10&category={category_id}&difficulty={difficulty}&type=multiple"
    
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
                question["id"] = number
                number += 1
                questions_data.append(question)
            
            number = 1
            return questions_data

        # If the request was not successful, return an error message
        return jsonify({'error': 'Failed to fetch questions'}), response.status_code

    except Exception as error:
        # Handle exceptions, such as connection errors
        return jsonify({'error': str(error)}), 500

def is_valid_image_url(url):
    """check if image is valid or not"""
    # info message
    message = ''
    
    try:
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code != 200:
            message = f"Failed to retrieve image. Status code: {response.status_code}"
            return False, message

        img = Image.open(BytesIO(response.content))
        
        # Check image format (convert to lowercase for case-insensitive comparison)
        if img.format.lower() not in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
            message = "Unsupported image format"
            return False, message

        # Check image file size using the content-length header
        max_file_size_mb = 5
        content_length = response.headers.get('content-length')
        
        if content_length is not None and int(content_length) > max_file_size_mb * 1024 * 1024:
            message = f"Image file size exceeds the allowed limit ({max_file_size_mb} MB)"
            return False, message
        
        return True, message
    
    except Exception as error:
        message = f"Error validating image URL: {error}"
        return False, message

    
import re
from database import users_collection


def is_valid_password(password):

    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    return re.match(pattern, password)


def register_user(username, password):

    existing = users_collection.find_one(
        {"username": username}
    )

    if existing:
        return {
            "message": "User already exists"
        }

    if not is_valid_password(password):
        return {
            "message": "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character."
        }

    users_collection.insert_one({
        "username": username,
        "password": password
    })

    return {
        "message": "Registration successful"
    }


def login_user(username, password):

    user = users_collection.find_one({
        "username": username,
        "password": password
    })

    if user:
        return {
            "message": "Login successful"
        }

    return {
        "message": "Invalid credentials"
    }
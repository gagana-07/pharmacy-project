import re
import bcrypt

from database import (
    users_collection,
    companies_collection
)


def hash_password(password):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password, hashed_password):

    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )


def is_valid_password(password):

    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    return re.match(pattern, password)


def register_user(
    username,
    password,
    company_code
):

    existing = users_collection.find_one(
        {"username": username}
    )

    if existing:
        return {
            "message": "User already exists"
        }

    company = companies_collection.find_one(
        {"company_code": company_code}
    )

    if not company:
        return {
            "message": "Invalid company code"
        }

    if not is_valid_password(password):
        return {
            "message": "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character."
        }

    users_collection.insert_one({
        "username": username,
        "password": hash_password(password),
        "company_code": company_code,
        "role": "staff",
        "status": "pending"
    })

    return {
        "message": "Registration submitted for approval"
    }


def login_user(
    username,
    password
):

    user = users_collection.find_one(
        {"username": username}
    )

    if not user:
        return {
            "message": "Invalid credentials"
        }

    if user["status"] != "approved":
        return {
            "message": "Account not approved"
        }

    if verify_password(
        password,
        user["password"]
    ):
        return {
            "message": "Login successful",
            "role": user["role"]
        }

    return {
        "message": "Invalid credentials"
    }
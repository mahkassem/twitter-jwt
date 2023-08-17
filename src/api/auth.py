from flask import Blueprint, jsonify, abort, request

from flask import current_app as app
from ..models import User
import hashlib
import secrets
import jwt


# Define a function to check if the given password is valid
def check_password(password: str, user: User):
    """Check if the given password is valid"""
    # salt = secrets.token_hex(16)
    salt =  app.config["SECRET_KEY"]
    return (
        user.password
        == hashlib.sha512((password + salt).encode("utf-8")).hexdigest()
    )


# Create a blueprint for the auth route
bp = Blueprint("auth", __name__, url_prefix="/auth")


# Define a route for logging in
@bp.route("/login", methods=["POST"])
def login():
    # Check if 'username' and 'password' keys are present
    if "username" not in request.json or "password" not in request.json:
        return abort(400, "username and password keys are required")
    # Get the values of 'username' and 'password'
    username = request.json["username"]
    password = request.json["password"]
    # Get the user with the given username
    user = User.query.filter_by(username=username).first()
    if user is None:
        return abort(404, "user not found")
    # Check if the given password is valid
    valid = check_password(password, user)
    if not valid:
        return abort(401, "invalid password")
    # Create a token for the user (JWT)
    token = jwt.encode(
        {"id": user.id},  # payload
        app.config["SECRET_KEY"],  # secret key
        algorithm="HS256",  # algorithm
    )
    return jsonify({"token": token})

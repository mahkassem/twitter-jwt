from flask import Blueprint, jsonify, abort, request
from flask import current_app as app
from ..models import User, db, Tweet, likes_table
import hashlib
import secrets


# Define a function to hash and salt the given password

def scramble(password: str):
    """Hash and salt the given password"""
    salt = app.config["SECRET_KEY"]
    return hashlib.sha512((password + salt).encode("utf-8")).hexdigest()


# Create a blueprint for the users route

bp = Blueprint("users", __name__, url_prefix="/users")


# Define a route for getting all users

@bp.route("", methods=["GET"])  # decorator takes path and list of HTTP verbs
def index():
    users = User.query.all()  # ORM performs SELECT query
    result = []
    for u in users:
        result.append(u.serialize())  # build list of users as dictionaries
    return jsonify(result)  # return JSON response


# Define a route for getting a specific user


@bp.route("/<int:id>", methods=["GET"])
def show(id: int):
    u = User.query.get_or_404(id)
    return jsonify(u.serialize())


# Define a route for creating a new user

@bp.route("", methods=["POST"])
def create():
    # Check if 'username' and 'password' keys are present
    if "username" not in request.json or "password" not in request.json:
        return abort(400)  # Return 400 Bad Request if keys are missing

    # Get the values of 'username' and 'password'
    username = request.json["username"]
    password = request.json["password"]

    # Check the length of username and password
    if len(username) < 3 or len(password) < 8:
        # Return 400 Bad Request if length of un is less than three characters
        # or passowrd is less than eight characters
        return abort(400)

    # Construct User
    u = User(username=username, password=scramble(request.json["password"]))
    db.session.add(u)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(u.serialize())

# Define a route for deleting a user

@bp.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    u = User.query.get_or_404(id)
    try:
        db.session.delete(u)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


# Define a route for updating a user


@bp.route("/<int:id>", methods=["PATCH", "PUT"])
def update(id):
    u = User.query.get_or_404(id)
    # Check if username and password are provided
    if "username" not in request.json and "password" not in request.json:
        abort(400)

    # Update username if provided
    if "username" in request.json:
        username = request.json["username"]
        if len(username) < 3:
            abort(400)
        u.username = username

    # Update password if provided
    if "password" in request.json:
        password = request.json["password"]
        if len(password) < 8:
            abort(400)
        u.password = scramble(password)
    try:
        db.session.commit()
        return jsonify(u.serialize())
    except:
        return jsonify(False)


# Define a route for getting the liked tweets of a user


@bp.route("/<int:id>/liked_tweets", methods=["GET"])
def liked_tweets(id):
    u = User.query.get_or_404(id)
    liked_tweets = u.liked_tweets

    return jsonify([t.serialize() for t in liked_tweets])

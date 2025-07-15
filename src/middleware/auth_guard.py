""" JWT Authentication """
import jwt
from functools import wraps
from flask import request, abort, current_app as app
from ..models import User


def auth_guard(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if 'Authorization' header is present
        # Authorization: Brearer <token>
        if "Authorization" in request.headers:
            # If present, get the token
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            # If not present, return 401 Unauthorized
            return abort(401, "Unauthorized")

        # Decode the token
        try:
            token = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            # If token is invalid, return 401 Unauthorized
            return abort(401, "Invalid token")

        # Get the user with the given id
        user = User.query.get(token["id"])

        if user is None:
            # If no user found, return 401 Unauthorized
            return abort(401, "Invalid token")

        # Call the function
        return f(user, *args, **kwargs)

    # Proceed to the route
    return decorated

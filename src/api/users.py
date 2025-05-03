from flask import Blueprint, jsonify, abort, request
from ..models import User,db
from flask import current_app as app
import hashlib

def scramble(password: str):
    """Hash and salt the given password"""
    salt = app.config["SECRET_KEY"]
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    users  = User.query.all()  # ORM performs SELECT query
    result = []
    for u in users:
        result.append(u.serialize())  # build list of Users  as dictionaries
    return jsonify(result)  # return JSON response

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    t = User.query.get_or_404(id, "Users not found")
    return jsonify(t.serialize())

@bp.route('', methods=['POST'])
def create():
    # req body must contain username and password
    if 'username' not in request.json or 'password' not in request.json:
        return abort(400)

    def user():
        username = request.json['username']
        password = request.json['password']

        if len(username) < 3 or len(password) < 8:
            abort(400)

    user()

    # construct User
    u = User(
        username=request.json['username'],
        password=scramble(request.json['password'])
    )

    db.session.add(u)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement

    return jsonify(u .serialize())



@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    u = User.query.get_or_404(id, "User not found")
    try:
        db.session.delete(u)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
    
@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    u = User.query.get_or_404(id)
    if 'username' not in request.json or 'password' not in request.json:
        return abort(400)

    def user_update():
        username = request.json['username']
        password = request.json['password']

        if len(username) < 3:
            return abort(400)

        if len(password) < 8:
            return abort(400)
        else:
            u.password = scramble(request.json['password'])

    user_update()
    
    try:
        db.session.commit()  
        return jsonify(True)
    except:
        return jsonify(False)
    
    
@bp.route('/<int:id>/liked_tweets', methods=['GET'])
def liked_tweets(id: int):
    u  = User.query.get_or_404(id)
    result = []
    for t in u .liked_tweets:
        result.append(t.serialize())
    return jsonify(result)
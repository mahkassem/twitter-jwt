from flask import Blueprint, jsonify, abort, request
from ..models import Tweet, User, db
from ..middleware.auth_guard import auth_guard


bp = Blueprint('tweets', __name__, url_prefix='/tweets')


@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    tweets = Tweet.query.all()  # ORM performs SELECT query
    result = []
    for t in tweets:
        result.append(t.serialize())  # build list of Tweets as dictionaries
    return jsonify(result)  # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    t = Tweet.query.get_or_404(id)
    return jsonify(t.serialize())


@bp.route('', methods=['POST'])
@auth_guard
def create(user: User):
    # req body must contain user_id and content
    if 'content' not in request.json:
        return abort(400)
    # construct Tweet
    t = Tweet(
        user_id=user.id,
        content=request.json['content']
    )
    db.session.add(t)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(t.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
@auth_guard
def delete(user: User, id: int):
    t = Tweet.query.get_or_404(id)
    
    # user must be the owner of the tweet
    if t.user_id != user.id:
        return abort(403, "Forbidden")
    
    try:
        db.session.delete(t)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>/liking_users', methods=['GET'])
def liking_users(id: int):
    t = Tweet.query.get_or_404(id)
    result = []
    for u in t.liking_users:
        result.append(u.serialize())
    return jsonify(result)

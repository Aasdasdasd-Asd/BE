from flask import Blueprint
from flask import request
from flask import jsonify

from project.controller.auth import AuthController
from flask_jwt_extended import (jwt_required)

bp = Blueprint("auth", __name__, url_prefix="/api")

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.


@bp.route("/register", methods=["POST"])
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    username = request.json["username"]
    password = request.json["password"]
    AuthController().register(username, password)

    return jsonify({'result': 'done'}), 200


@bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json["username"]
    password = request.json["password"]
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    return AuthController().login(username, password)


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.

@bp.route("/logout", methods=['POST'])
def logout():
    """Clear the current session, including the stored user id."""
    AuthController().logout()
    return jsonify({'result': 'done'}), 200


@bp.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = AuthController().protected()
    return jsonify(logged_in_as=current_user), 200

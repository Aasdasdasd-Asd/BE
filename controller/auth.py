from project import db
from project.models.auth import User
from flask import jsonify
from flask import session
from flask_jwt_extended import (create_access_token, get_jwt_identity)


class AuthController:
    def __init__(self):
       pass

    def register(self, username, password):
        """Register a new user.

        Validates that the username is not already taken. Hashes the
        password for security.
        """
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif db.session.query(
                User.query.filter_by(username=username).exists()
        ).scalar():
            error = f"User {username} is already registered."

        if error is None:
            # the name is available, create the user and go to the login page
            db.session.add(User(username=username, password=password))
            db.session.commit()

    def login(self, username, password):
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            return jsonify({"msg": "Incorrect username."}), 400
        elif not user.check_password(password):
            return jsonify({"msg": "Incorrect password."}), 400

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user.id
            # Identity can be any data that is json serializable
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200

    def logout(self):
        """Clear the current session, including the stored user id."""
        session.clear()

    def protected(self):
        # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()
        return current_user

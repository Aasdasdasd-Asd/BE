from flask import Blueprint
from flask import request
from flask import jsonify
from project.controller.blog import BlogController
from flask_jwt_extended import (jwt_required)


bp = Blueprint("blog", __name__, url_prefix="/api")


@bp.route("/")
@jwt_required
def index():
    """Show all the posts, most recent first."""
    list_post = BlogController().index()

    return jsonify({'result': list_post})


@bp.route("/create", methods=["POST"])
@jwt_required
def create():
    """Create a new post for the current user."""
    title = request.json["title"]
    body = request.json["content"]
    BlogController().create(title, body)

    return jsonify({'msg': 'done'}), 200


@bp.route("/update", methods=["PUT"])
@jwt_required
def update():
    """Update a post if the current user is the author."""
    id = request.json["id"]
    title = request.json["title"]
    body = request.json["content"]
    BlogController().update(id, title, body)

    return jsonify({'msg': 'done'}), 200


@bp.route("/delete/<id>", methods=["DELETE"])
@jwt_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    BlogController().delete(id)

    return jsonify({'msg': 'done'}), 200


@bp.route("/search/<title>", methods=["GET"])
@jwt_required
def search(title):
    """Search post by title"""
    list_post = BlogController().search(title)

    return jsonify({'result': list_post})

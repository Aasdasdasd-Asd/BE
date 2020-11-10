from flask import flash

from project.models.blog import Post
from project import db


class BlogController:
    def __init__(self):
        pass

    def index(sefl):
        """Show all the posts, most recent first."""
        # per_page = 2
        # posts = Post.query.order_by(Post.created.desc()).paginate(page, per_page, error_out=False)
        posts = Post.query.order_by(Post.created.desc()).all()
        list_post = []
        for post in posts:
            a = {
                "id": post.id,
                "title": post.title,
                "content": post.body
            }
            list_post.append(a)
        return list_post

    def create(self, title, body):
        """Create a new post for the current user."""
        db.session.add(Post(title=title, body=body))
        db.session.commit()

    def update(self, id, title, body):
        """Update a post if the current user is the author."""
        post = Post.query.get_or_404(id)
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.commit()

    def delete(self, id):
        """Delete a post.

        Ensures that the post exists and that the logged in user is the
        author of the post.
        """
        post = Post.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()

    def search(self, title):
        """Search post by title"""
        posts = Post.query.filter(Post.title.like('%' + title + '%'))
        posts = posts.order_by(Post.created.desc()).all()
        list_post = []
        for post in posts:
            a = {
                "id": post.id,
                "title": post.title,
                "content": post.body
            }
            list_post.append(a)
        return list_post

from flask import url_for

from project import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)

    # User object backed by author_id
    # lazy="joined" means the user is returned with the post in one query

    @property
    def update_url(self):
        return url_for("blog.update", id=self.id)

    @property
    def delete_url(self):
        return url_for("blog.delete", id=self.id)

from sqlalchemy.sql import func

from project import db


# model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

    def to_json(self):
        return dict(
            username=self.username,
            email=self.email,
            active=self.active,
            id=self.id
        )

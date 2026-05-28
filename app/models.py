from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    author = db.Column(
        db.String(200),
        nullable=False
    )

    total_pages = db.Column(
        db.Integer,
        nullable=False
    )

    current_page = db.Column(
        db.Integer,
        default=0
    )

    status = db.Column(
        db.String(50),
        default="Reading"
    )
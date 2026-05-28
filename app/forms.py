from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SubmitField
)

from wtforms.validators import DataRequired


class BookForm(FlaskForm):

    title = StringField(
        "Book Title",
        validators=[DataRequired()]
    )

    author = StringField(
        "Author",
        validators=[DataRequired()]
    )

    total_pages = IntegerField(
        "Total Pages",
        validators=[DataRequired()]
    )

    current_page = IntegerField(
        "Current Page",
        validators=[DataRequired()]
    )

    submit = SubmitField("Save")
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash
)

import os

from app.forms import BookForm
from app.models import Book, db


app = Flask(__name__)

app.config["SECRET_KEY"] = "secretkey"

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
with app.app_context():
    db.create_all()


# HOME / DASHBOARD
@app.route("/", methods=["GET", "POST"])
def dashboard():

    form = BookForm()

    # HANDLE FORM SUBMISSION
    if form.validate_on_submit():

        status = "Reading"

        if form.current_page.data >= form.total_pages.data:
            status = "Completed"

        book = Book(
            title=form.title.data,
            author=form.author.data,
            total_pages=form.total_pages.data,
            current_page=form.current_page.data,
            status=status
        )

        db.session.add(book)

        db.session.commit()

        flash(
            "Book added successfully!",
            "success"
        )

        return redirect(
            url_for("dashboard")
        )

    books = Book.query.all()

    return render_template(
        "dashboard.html",
        books=books,
        form=form
    )


# VIEW SINGLE BOOK
@app.route("/books/<int:id>")
def view_book(id):

    book = Book.query.get_or_404(id)

    return render_template(
        "book_details.html",
        book=book
    )


# EDIT BOOK
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_book(id):

    book = Book.query.get_or_404(id)

    form = BookForm(obj=book)

    if form.validate_on_submit():

        book.title = form.title.data

        book.author = form.author.data

        book.total_pages = form.total_pages.data

        book.current_page = form.current_page.data

        if book.current_page >= book.total_pages:
            book.status = "Completed"
        else:
            book.status = "Reading"

        db.session.commit()

        flash(
            "Book updated successfully!",
            "info"
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "edit_book.html",
        form=form,
        book=book
    )


# DELETE BOOK
@app.route("/delete/<int:id>", methods=["POST"])
def delete_book(id):

    book = Book.query.get_or_404(id)

    db.session.delete(book)

    db.session.commit()

    flash(
        "Book deleted successfully!",
        "danger"
    )

    return redirect(
        url_for("dashboard")
    )


@app.route("/health")
def health():
    return {
        "status": "healthy"
    }, 200

if __name__ == "__main__":

    

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

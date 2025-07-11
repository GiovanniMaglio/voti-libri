from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Scegliamo PostgreSQL se DATABASE_URL è settata, altrimenti SQLite in locale
db_url = os.getenv("DATABASE_URL", "sqlite:///libri.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modello libro
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.Text)
    owner = db.Column(db.String(100))
    added_on = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def index():
    all_books = Book.query.order_by(Book.added_on.desc()).all()
    miei = [b for b in all_books if (b.owner or "").lower() == "giovanni maglio"]
    altri = [b for b in all_books if (b.owner or "").lower() != "giovanni maglio"]
    return render_template("index.html", my_books=miei, other_books=altri)

@app.route("/add", methods=["POST"])
def add_book():
    data = request.form
    book = Book(
        title=data["title"],
        author=data["author"],
        rating=float(data["rating"]),
        review=data["review"],
        owner=data.get("owner", "Anonimo").strip()
    )
    db.session.add(book)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/libro/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("book.html", book=book)

@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
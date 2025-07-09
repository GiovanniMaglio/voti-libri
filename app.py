from __future__ import annotations
import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

def _normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql") and "sslmode" not in url:
        url += "?sslmode=require"
    return url

_db_uri = _normalize_database_url(os.getenv("DATABASE_URL", "sqlite:///libri.db"))

app.config.update(
    SQLALCHEMY_DATABASE_URI=_db_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db = SQLAlchemy(app)
print("🔌 Connessione DB usata:", _db_uri)

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.Text)
    owner = db.Column(db.String(100))
    added_on = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def index():
    all_books = Book.query.all()
    miei_libri = [b for b in all_books if (b.owner or "").lower() == "giovanni maglio"]
    altri_libri = [b for b in all_books if (b.owner or "").lower() != "giovanni maglio"]
    return render_template("index.html", my_books=miei_libri, other_books=altri_libri)

@app.route("/add", methods=["POST"])
def add_book():
    title = request.form["title"]
    author = request.form["author"]
    rating = float(request.form["rating"])
    review = request.form["review"]
    owner = request.form.get("owner", "").strip() or "Anonimo"
    new_book = Book(title=title, author=author, rating=rating, review=review, owner=owner, added_on=datetime.utcnow())
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/libro/<int:book_id>")
def book_detail(book_id: int):
    book = Book.query.get_or_404(book_id)
    return render_template("book.html", book=book)

@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id: int):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("index"))

def create_db_if_needed() -> None:
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database pronto o già esistente.")
        except Exception as exc:
            print("❌ Errore nel creare le tabelle:", exc)

create_db_if_needed()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🚀 Avvio in locale su http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)

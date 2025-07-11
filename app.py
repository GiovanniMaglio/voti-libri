from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista dei libri in memoria
books = []

@app.route("/")
def index():
    miei_libri = [b for b in books if (b["owner"] or "").lower() == "giovanni maglio"]
    altri_libri = [b for b in books if (b["owner"] or "").lower() != "giovanni maglio"]
    return render_template("index.html", my_books=miei_libri, other_books=altri_libri)

@app.route("/add", methods=["POST"])
def add_book():
    title = request.form["title"]
    author = request.form["author"]
    rating = float(request.form["rating"])
    review = request.form["review"]
    owner = request.form.get("owner", "").strip() or "Anonimo"

    book = {
        "id": len(books) + 1,
        "title": title,
        "author": author,
        "rating": rating,
        "review": review,
        "owner": owner,
    }
    books.append(book)
    return redirect(url_for("index"))

@app.route("/libro/<int:book_id>")
def book_detail(book_id):
    for book in books:
        if book["id"] == book_id:
            return render_template("book.html", book=book)
    return "Libro non trovato", 404

@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    global books
    books = [book for book in books if book["id"] != book_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
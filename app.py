from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# 🔧 Inizializza il database
def init_db():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            rating REAL NOT NULL,
            review TEXT,
            owner TEXT,
            added_on TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("SELECT id, title, author, rating, review, owner FROM books")
    all_books = c.fetchall()
    conn.close()

    miei_libri = [b for b in all_books if (b[5] or "").lower() == "giovanni maglio"]
    altri_libri = [b for b in all_books if (b[5] or "").lower() != "giovanni maglio"]

    return render_template("index.html", my_books=miei_libri, other_books=altri_libri)

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    rating = float(request.form['rating'])
    review = request.form['review']
    owner = request.form.get('owner', '').strip() or "Anonimo"
    now = datetime.now().isoformat()

    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('INSERT INTO books (title, author, rating, review, owner, added_on) VALUES (?, ?, ?, ?, ?, ?)',
              (title, author, rating, review, owner, now))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/libro/<int:book_id>')
def book_detail(book_id):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('SELECT title, author, rating, review, owner FROM books WHERE id = ?', (book_id,))
    book = c.fetchone()
    conn.close()
    return render_template('book.html', book=book)

@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
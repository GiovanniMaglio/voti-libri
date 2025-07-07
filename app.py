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
            review TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS newsletter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            subscribed_on TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 🏠 Homepage: lista dei libri
@app.route('/')
def index():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('SELECT id, title, author, rating FROM books')
    books = c.fetchall()
    conn.close()
    return render_template('index.html', books=books)

# ➕ Aggiungi libro
@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    rating = float(request.form['rating'])
    review = request.form['review']

    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('INSERT INTO books (title, author, rating, review) VALUES (?, ?, ?, ?)',
              (title, author, rating, review))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# 📄 Dettaglio libro
@app.route('/libro/<int:book_id>')
def book_detail(book_id):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('SELECT title, author, rating, review FROM books WHERE id = ?', (book_id,))
    book = c.fetchone()
    conn.close()
    return render_template('book.html', book=book)

# 📩 Iscrizione newsletter
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    now = datetime.now().isoformat()

    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO newsletter (email, subscribed_on) VALUES (?, ?)', (email, now))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Email già registrata
    conn.close()
    return redirect(url_for('index'))

# 🗑️ Elimina libro
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
    app.run(debug=False, host='0.0.0.0')
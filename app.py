from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


app = Flask(__name__)

# 🔧 Configurazione database PostgreSQL (Supabase)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:FisicaStatale2024@rujiwukbcoexouvsuyhg.supabase.co:5432/postgres'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

print("Connessione DB usata:", app.config['SQLALCHEMY_DATABASE_URI'])  # stampa di debug

# 📚 Modello Book
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.Text)
    owner = db.Column(db.String(100))
    added_on = db.Column(db.DateTime, default=datetime.utcnow)

# 🌐 Homepage
@app.route('/')
def index():
    all_books = Book.query.all()
    miei_libri = [b for b in all_books if (b.owner or "").lower() == "giovanni maglio"]
    altri_libri = [b for b in all_books if (b.owner or "").lower() != "giovanni maglio"]
    return render_template("index.html", my_books=miei_libri, other_books=altri_libri)

# ➕ Aggiungi libro
@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    rating = float(request.form['rating'])
    review = request.form['review']
    owner = request.form.get('owner', '').strip() or "Anonimo"

    new_book = Book(
        title=title,
        author=author,
        rating=rating,
        review=review,
        owner=owner,
        added_on=datetime.now()
    )
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('index'))

# 📖 Dettaglio libro
@app.route('/libro/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', book=book)

# ❌ Elimina libro
@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))


from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


app = Flask(__name__)

# 🔧 Configurazione database PostgreSQL (Supabase)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///libri.db'  # fallback locale se non trova DATABASE_URL
)    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

print("Connessione DB usata:", app.config['SQLALCHEMY_DATABASE_URI'])  # stampa di debug

# 📚 Modello Book
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.Text)
    owner = db.Column(db.String(100))
    added_on = db.Column(db.DateTime, default=datetime.utcnow)

# 🌐 Homepage
@app.route('/')
def index():
    all_books = Book.query.all()
    miei_libri = [b for b in all_books if (b.owner or "").lower() == "giovanni maglio"]
    altri_libri = [b for b in all_books if (b.owner or "").lower() != "giovanni maglio"]
    return render_template("index.html", my_books=miei_libri, other_books=altri_libri)

# ➕ Aggiungi libro
@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    rating = float(request.form['rating'])
    review = request.form['review']
    owner = request.form.get('owner', '').strip() or "Anonimo"

    new_book = Book(
        title=title,
        author=author,
        rating=rating,
        review=review,
        owner=owner,
        added_on=datetime.now()
    )
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('index'))

# 📖 Dettaglio libro
@app.route('/libro/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', book=book)

# ❌ Elimina libro
@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))


# ▶️ Avvio
if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
        print("Database connesso e tabelle create")
    except Exception as e:
        print("Errore di connessione al DB:", e)

    # Avvia il server Flask
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
import os
import requests
from flask import Flask, render_template,session,request,redirect,url_for,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key='HelloHacker
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def red():
    return redirect(url_for('index'))


@app.route("/index")
def index():
    if 'user_id' in session:
        session.pop('user_id',None)
    return render_template('index.html')

@app.route("/login",methods=['POST'])
def login():
    username=request.form.get("username1")
    password=request.form.get("password1")
    user=db.execute("SELECT * FROM users WHERE username=:username AND pw=:pw",{"username":username,"pw":password}).fetchone()
    if user is not None:
        session['user_id']=user.id
        global g
        g=user
        books=db.execute("SELECT * FROM books").fetchall()
        return render_template('search.html',books=books)
    else:
        return redirect(url_for('index'))  
@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/success",methods=['POST'])
def success():
    try:
        username=request.form.get("username")
        password=request.form.get("password")
        db.execute("INSERT INTO users(username,pw) VALUES (:username,:pw)",{"username":username,"pw":password})
        db.commit()
        return render_template('success.html')
    except ValueError:
        redirect(url_for('register'))


@app.route("/search/<string:isbn>")
def book(isbn):
    if g.id == session['user_id']:
        book=db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
        res=requests.get("https://www.goodreads.com/book/review_counts.json",params={"key":"IV1jBSOeIKfZKv0aEL1XkQ","isbns":isbn})
        book_rev=res.json()
        avg=book_rev["books"][0]["average_rating"]
        num=book_rev["books"][0]["work_ratings_count"]
        reviews=db.execute("SELECT * FROM reviews WHERE isbn=:isbn",{"isbn":isbn}).fetchall()
        c=0
        for review in reviews:
            if g.username==review.username:
                c=1
        return render_template('book.html',book=book,avg=avg,num=num,user=g,reviews=reviews,c=c)
    else:
        return redirect(url_for('index'))

@app.route("/search/<string:isbn>/review",methods=['POST'])
def review_(isbn):
    if g.id == session['user_id']:
        rev=request.form.get('review')
        rating=request.form.get('rating')
        db.execute("INSERT INTO reviews(isbn,username,review,rating) VALUES (:isbn,:username,:review,:rating)",{"isbn":isbn,"username":g.username,"review":rev,"rating":rating})
        db.commit()
        return redirect(url_for('book',isbn=isbn))
    else:
        return redirect(url_for('index'))
@app.route("/search/back")
def back():
    if g.id == session['user_id']:
        books=db.execute("SELECT * FROM books").fetchall()
        return render_template('search.html',books=books)
    else:
        return redirect(url_for('index'))

@app.route("/search/result", methods=['POST'])
def search():
    if g.id == session['user_id']:
        text_=request.form.get('text_')
        books_=db.execute("SELECT * FROM books WHERE isbn LIKE :s OR title LIKE :s OR author LIKE :s",{'s':f'%{text_}%'}).fetchall()
        return render_template('result.html',books=books_)
    else:
        return redirect(url_for('index'))    

@app.route("/api/<string:isbn>")
def json(isbn):
    book=db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
    if book is None:
        return jsonify({"error": "Invalid ISBN Number"}),404
    else:
        res=requests.get("https://www.goodreads.com/book/review_counts.json",params={"key":"IV1jBSOeIKfZKv0aEL1XkQ","isbns":isbn})
        book_rev=res.json()
        avg=book_rev["books"][0]["average_rating"]
        num=book_rev["books"][0]["work_ratings_count"]
        return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": num,
        "average_score": avg 
        })

if __name__ == "__main__":
    app.run()

    

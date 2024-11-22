from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Book

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        genre = request.form.get("genre")
        year = request.form.get("year")
        if title and author:
            new_book = Book(title=title, author=author, genre=genre, year=year)
            db.session.add(new_book)
            db.session.commit()
            flash('Sách đã được thêm!', 'success')
        return redirect(url_for('main.index'))

    books = Book.query.all()
    return render_template("index.html", books=books)

@main.route("/edit/<int:id>", methods=["POST"])
@login_required
def edit_book(id):
    book = Book.query.get_or_404(id)
    book.title = request.form.get("title")
    book.author = request.form.get("author")
    book.genre = request.form.get("genre")
    book.year = request.form.get("year")
    db.session.commit()
    flash('Sách đã được cập nhật!', 'success')
    return redirect(url_for('main.index'))

@main.route("/delete/<int:id>")
@login_required
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Sách đã bị xóa!', 'success')
    return redirect(url_for('main.index'))

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash('Email đã tồn tại!', 'danger')
            return redirect(url_for('main.register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Đăng ký thành công! Bạn có thể đăng nhập.', 'success')
        return redirect(url_for('main.login'))

    return render_template("register.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Email hoặc mật khẩu không đúng!', 'danger')
            return redirect(url_for('main.login'))
        login_user(user)
        flash('Đăng nhập thành công!', 'success')
        return redirect(url_for('main.index'))

    return render_template("login.html")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất.', 'success')
    return redirect(url_for('main.login'))

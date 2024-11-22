from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Book

# Định nghĩa Blueprint
main = Blueprint('main', __name__)


@main.route("/", methods=["GET", "POST"])
@login_required
def index():
    """
    Trang chính quản lý sách. Hỗ trợ thêm sách và hiển thị danh sách sách.
    """
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        genre = request.form.get("genre")
        year = request.form.get("year")

        # Kiểm tra thông tin đầu vào
        if not title or not author:
            flash('Tiêu đề và tác giả là bắt buộc!', 'danger')
            return redirect(url_for('main.index'))

        # Thêm sách vào cơ sở dữ liệu
        try:
            new_book = Book(title=title, author=author, genre=genre, year=year)
            db.session.add(new_book)
            db.session.commit()
            flash('Sách đã được thêm thành công!', 'success')
        except Exception as e:
            flash(f'Đã xảy ra lỗi khi thêm sách: {str(e)}', 'danger')
        return redirect(url_for('main.index'))

    books = Book.query.all()
    return render_template("index.html", books=books)


@main.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_book(id):
    """
    Chỉnh sửa thông tin sách dựa trên ID.
    """
    book = Book.query.get_or_404(id)

    if request.method == "POST":
        book.title = request.form.get("title")
        book.author = request.form.get("author")
        book.genre = request.form.get("genre")
        book.year = request.form.get("year")

        try:
            db.session.commit()
            flash('Sách đã được cập nhật thành công!', 'success')
        except Exception as e:
            flash(f'Đã xảy ra lỗi khi cập nhật sách: {str(e)}', 'danger')
        return redirect(url_for('main.index'))

    return render_template("edit_book.html", book=book)


@main.route("/delete/<int:id>")
@login_required
def delete_book(id):
    """
    Xóa sách dựa trên ID.
    """
    book = Book.query.get_or_404(id)

    try:
        db.session.delete(book)
        db.session.commit()
        flash('Sách đã bị xóa thành công!', 'success')
    except Exception as e:
        flash(f'Đã xảy ra lỗi khi xóa sách: {str(e)}', 'danger')

    return redirect(url_for('main.index'))


@main.route("/register", methods=["GET", "POST"])
def register():
    """
    Trang đăng ký người dùng mới.
    """
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Kiểm tra các trường không được để trống
        if not username or not email or not password:
            flash('Vui lòng điền đầy đủ thông tin!', 'danger')
            return redirect(url_for('main.register'))

        # Kiểm tra email đã tồn tại
        if User.query.filter_by(email=email).first():
            flash('Email đã tồn tại!', 'danger')
            return redirect(url_for('main.register'))

        # Kiểm tra username đã tồn tại
        if User.query.filter_by(username=username).first():
            flash('Tên đăng nhập đã tồn tại!', 'danger')
            return redirect(url_for('main.register'))

        # Kiểm tra độ dài mật khẩu
        if len(password) < 6:
            flash('Mật khẩu phải có ít nhất 6 ký tự!', 'danger')
            return redirect(url_for('main.register'))

        # Tạo người dùng mới
        try:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email,
                            password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Đăng ký thành công! Bạn có thể đăng nhập.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            flash(f'Đã xảy ra lỗi khi đăng ký: {str(e)}', 'danger')

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    """
    Trang đăng nhập người dùng.
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        # Kiểm tra email và mật khẩu
        if not user or not check_password_hash(user.password, password):
            flash('Email hoặc mật khẩu không đúng!', 'danger')
            return redirect(url_for('main.login'))

        # Đăng nhập thành công
        login_user(user)
        flash('Đăng nhập thành công!', 'success')
        return redirect(url_for('main.index'))

    return render_template("login.html")


@main.route("/logout")
@login_required
def logout():
    """
    Đăng xuất người dùng.
    """
    logout_user()
    flash('Bạn đã đăng xuất.', 'success')
    return redirect(url_for('main.login'))

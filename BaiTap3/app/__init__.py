from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Khởi tạo các tiện ích
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Nạp cấu hình từ config.py

    # Khởi tạo các tiện ích với ứng dụng Flask
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Cấu hình login view
    login_manager.login_view = 'main.login'

    # Đăng ký blueprint
    from app.views import main
    app.register_blueprint(main)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))  # Tìm User theo id

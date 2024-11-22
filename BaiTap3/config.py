import os

class Config:
    # Kết nối PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@127.0.0.1:5432/quanlysach'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # Tạo khóa bảo mật cho Flask

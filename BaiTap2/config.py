import psycopg2


def connect_db():
    return psycopg2.connect(
        host='127.0.0.1',
        user='postgres',
        password='123456',
        dbname='quanlysinhvien'
    )

from config import connect_db


def fetch_students():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_student(name, age, gender, email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, age, gender, email) VALUES (%s, %s, %s, %s)",
        (name, age, gender, email)
    )
    conn.commit()
    conn.close()


def delete_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    conn.close()

# Tùy chọn thêm các hàm như update_student nếu cần


def update_student(student_id, name, age, gender, email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students SET name = %s, age = %s, gender = %s, email = %s WHERE id = %s",
        (name, age, gender, email, student_id)
    )
    conn.commit()
    conn.close()

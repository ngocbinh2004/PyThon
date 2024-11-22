from model import fetch_students, add_student, delete_student
from view import StudentView
from tkinter import messagebox
import tkinter as tk


class StudentController:
    def __init__(self):
        self.view = StudentView(self)

    def refresh_students(self):
        students = fetch_students()
        self.view.populate_table(students)

    def add_student(self):
        form_data = self.view.get_form_data()
        name, age, gender, email = form_data["name"], form_data["age"], form_data["gender"], form_data["email"]

        if not name or not age or not gender or not email:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Error", "Age must be a number!")
            return

        add_student(name, age, gender, email)
        self.view.clear_form()
        self.refresh_students()

    def delete_student(self):
        selected_item = self.view.tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "No student selected!")
            return

        student_id = self.view.tree.item(selected_item)["values"][0]
        delete_student(student_id)
        self.refresh_students()

    def update_student(self):
        # Lấy sinh viên được chọn trong bảng
        selected_item = self.view.tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "No student selected!")
            return

        # Lấy thông tin sinh viên từ Treeview
        student_data = self.view.tree.item(selected_item)["values"]
        if not student_data:
            messagebox.showerror(
                "Error", "Could not fetch selected student's data!")
            return

        # Gán dữ liệu sinh viên vào các ô nhập liệu
        student_id, name, age, gender, email = student_data

        self.view.name_entry.delete(0, tk.END)
        self.view.name_entry.insert(0, name)

        self.view.age_entry.delete(0, tk.END)
        self.view.age_entry.insert(0, age)

        self.view.gender_entry.delete(0, tk.END)
        self.view.gender_entry.insert(0, gender)

        self.view.email_entry.delete(0, tk.END)
        self.view.email_entry.insert(0, email)

        # Lưu ID của sinh viên để sử dụng khi lưu thay đổi
        self.selected_student_id = student_id

    def save_changes(self):
        if not hasattr(self, "selected_student_id"):
            messagebox.showerror("Error", "No student selected for update!")
            return

        # Lấy dữ liệu mới từ form
        updated_data = self.view.get_form_data()
        updated_name = updated_data["name"]
        updated_age = updated_data["age"]
        updated_gender = updated_data["gender"]
        updated_email = updated_data["email"]

        # Kiểm tra dữ liệu hợp lệ
        if not updated_name or not updated_age or not updated_gender or not updated_email:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            updated_age = int(updated_age)  # Kiểm tra tuổi có phải số không
        except ValueError:
            messagebox.showerror("Error", "Age must be a number!")
            return

        # Gọi hàm cập nhật trong Model
        from model import update_student
        update_student(self.selected_student_id, updated_name,
                       updated_age, updated_gender, updated_email)

        # Làm mới bảng và xóa form
        self.refresh_students()
        self.view.clear_form()
        del self.selected_student_id  # Xóa ID sau khi cập nhật
        messagebox.showinfo(
            "Success", "Student information updated successfully!")

    def refresh_form(self):
        """Gọi clear_form từ View để làm sạch ô nhập liệu."""
        self.view.clear_form()

    def run(self):
        self.refresh_students()
        self.view.run()

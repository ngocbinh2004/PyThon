import tkinter as tk
from tkinter import ttk


class StudentView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Student Management")

        # Frame nhập liệu
        form_frame = tk.Frame(self.root)
        form_frame.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(form_frame, text="Name:").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Age:").grid(
            row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.age_entry = tk.Entry(form_frame)
        self.age_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Gender:").grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.gender_entry = tk.Entry(form_frame)
        self.gender_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Email:").grid(
            row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.email_entry = tk.Entry(form_frame)
        self.email_entry.grid(row=1, column=3, padx=5, pady=5)

        # Frame nút bấm
        button_frame = tk.Frame(self.root)
        button_frame.pack(padx=10, pady=10, fill=tk.X)

        tk.Button(button_frame, text="Add", command=self.controller.add_student,
                  width=12).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Delete", command=self.controller.delete_student,
                  width=12).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Refresh", command=self.controller.refresh_form,
                  width=12).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="Update", command=self.controller.update_student,
                  width=12).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(button_frame, text="Save Changes", command=self.controller.save_changes,
                  width=12).grid(row=0, column=4, padx=5, pady=5)

        # Frame hiển thị danh sách
        table_frame = tk.Frame(self.root)
        table_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Age", "Gender", "Email"),
            show="headings",
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Email", text="Email")
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Name", width=150)
        self.tree.column("Age", width=100, anchor=tk.CENTER)
        self.tree.column("Gender", width=100, anchor=tk.CENTER)
        self.tree.column("Email", width=200)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()

    def populate_table(self, students):
        # Xóa dữ liệu cũ
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Thêm dữ liệu mới
        for student in students:
            self.tree.insert("", tk.END, values=student)

    def get_form_data(self):
        return {
            "name": self.name_entry.get(),
            "age": self.age_entry.get(),
            "gender": self.gender_entry.get(),
            "email": self.email_entry.get(),
        }

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.gender_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

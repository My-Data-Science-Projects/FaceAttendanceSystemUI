import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
import shutil
from database import get_connection
from face_utils import capture_face

def student_management():
    win = ctk.CTkToplevel()
    win.title("Student Management")
    win.geometry("1000x600")
    win.lift()
    win.focus_force()
    win.attributes("-topmost", True)
    win.after(100, lambda: win.attributes("-topmost", False))

    frame = tk.Frame(win, bg="white")
    frame.pack(fill="both", expand=True)

    def refresh():
        for widget in frame.winfo_children():
            widget.destroy()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student WHERE is_delete=0")
        students = cursor.fetchall()
        conn.close()

        headers = ["ID", "Name", "Course", "Admission Date", "Action"]
        for i, text in enumerate(headers):
            label = tk.Label(frame, text=text, font=("Arial", 11, "bold"), bg="#cccccc", fg="black", width=20, borderwidth=1, relief="solid")
            label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        if not students:
            tk.Label(
                frame, text="No Records Found", font=("Arial", 12, "italic"),
                fg="gray", bg="white"
            ).grid(row=1, column=0, columnspan=5, pady=20)
            return

        for i, student in enumerate(students, start=1):
            for j, value in enumerate(student[:-1]):  # Exclude last column (folder name)
                label = tk.Label(frame, text=value, bg="#ffffff", fg="#000000",
                                 font=("Arial", 11), borderwidth=1, relief="solid", width=20)
                label.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)

            action_frame = tk.Frame(frame, bg="#ffffff", borderwidth=1, relief="solid")
            action_frame.grid(row=i, column=4, sticky="nsew", padx=1, pady=1)

            edit_btn = tk.Button(action_frame, text="Edit", bg="#4CAF50", fg="white",
                                 font=("Arial", 10), width=10, command=lambda s=student: edit_student(s))
            edit_btn.pack(side="left", padx=5, pady=5)

            delete_btn = tk.Button(action_frame, text="Delete", bg="#F44336", fg="white",
                                   font=("Arial", 10), width=10, command=lambda s=student: delete_student(s))
            delete_btn.pack(side="left", padx=5, pady=5)

    def edit_student(student):
        edit = ctk.CTkToplevel()
        edit.title("Edit Student")
        edit.geometry("400x400")
        edit.configure(fg_color="white")
        edit.lift()
        edit.focus_force()
        edit.attributes("-topmost", True)
        edit.after(100, lambda: edit.attributes("-topmost", False))

        label_font = ("Arial", 12, "bold")
        entry_font = ("Arial", 12)

        def create_labeled_entry(parent, label_text, default_value):
            ctk.CTkLabel(parent, text=label_text, text_color="black", font=label_font).pack(pady=(20, 5))
            entry = ctk.CTkEntry(parent, font=entry_font, width=300)
            entry.insert(0, default_value)
            entry.pack()
            return entry

        name_entry = create_labeled_entry(edit, "Name", student[1])
        course_entry = create_labeled_entry(edit, "Course", student[2])

        def save_changes():
            name = name_entry.get()
            course = course_entry.get()
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE student SET name=%s, course=%s WHERE id=%s", (name, course, student[0]))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student details updated successfully")
            edit.destroy()
            refresh()

        def update_face():
            folder_path = os.path.join("face_data", student[4])
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            capture_face(folder_path)
            messagebox.showinfo("Success", "Face data updated successfully")

        ctk.CTkButton(edit, text="Save", command=save_changes, font=("Arial", 12), fg_color="#4CAF50", width=150).pack(pady=(30, 10))
        ctk.CTkButton(edit, text="Update Face", command=update_face, font=("Arial", 12), fg_color="#2196F3", width=150).pack()

    def delete_student(student):
        if messagebox.askyesno("Confirm", "Delete student?"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE student SET is_delete=1 WHERE id=%s", (student[0],))
            conn.commit()
            conn.close()

            path = os.path.join("face_data", student[4])
            if os.path.exists(path):
                shutil.rmtree(path)

            messagebox.showinfo("Deleted", "Student deleted successfully")
            refresh()

    refresh()
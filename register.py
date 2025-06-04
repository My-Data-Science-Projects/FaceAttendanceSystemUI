import customtkinter as ctk
from tkinter import messagebox  # messagebox stays from tkinter
from datetime import datetime
import time
import os
from face_utils import capture_face
from database import get_connection

def register_page():
    reg = ctk.CTkToplevel()
    reg.title("Student Registration")
    reg.geometry("800x500")
    reg.configure(fg_color="white")
    reg.lift()
    reg.focus_force()
    reg.attributes("-topmost", True)
    reg.after(100, lambda: reg.attributes("-topmost", False))

    label_font = ("Arial", 12, "bold")
    entry_font = ("Arial", 12)

    def create_labeled_entry(parent, label_text):
        ctk.CTkLabel(parent, text=label_text, font=label_font, text_color="black").pack(pady=(20, 5))
        entry = ctk.CTkEntry(parent, font=entry_font, width=300, border_width=2, corner_radius=6)
        entry.pack()
        return entry

    entry_name = create_labeled_entry(reg, "Name:")
    entry_course = create_labeled_entry(reg, "Course:")

    def save_student():
        name = entry_name.get()
        course = entry_course.get()
        if not name or not course:
            messagebox.showerror("Error", "Please fill all fields")
            return

        timestamp = str(int(time.time()))
        folder_name = f"{name}_{timestamp}"
        admission_date = datetime.now().strftime("%Y-%m-%d")

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO student (name, course, admission_date, folder_name) VALUES (%s, %s, %s, %s)",
                (name, course, admission_date, folder_name)
            )
            conn.commit()
            conn.close()

            os.makedirs(os.path.join("face_data", folder_name), exist_ok=True)
            capture_face(os.path.join("face_data", folder_name))
            messagebox.showinfo("Success", "Student registered successfully")
            reg.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(reg, text="Register", command=save_student, font=("Arial", 12), fg_color="#4CAF50", text_color="white", width=150, height=40).pack(pady=30)

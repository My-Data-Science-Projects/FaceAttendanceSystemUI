import customtkinter as ctk
from tkinter import messagebox
import register
import attendance
import student_mgmt
import attendance_mgmt

def open_registration():
    register.register_page()

def open_mark_attendance():
    attendance.mark_attendance()

def open_student_mgmt():
    student_mgmt.student_management()

def open_attendance_mgmt():
    attendance_mgmt.attendance_management()

def main():
    ctk.set_appearance_mode("System")  # optional: "Dark", "Light"
    ctk.set_default_color_theme("blue")  # optional: "blue", "green", "dark-blue"

    root = ctk.CTk()
    root.title("Face Attendance System")
    root.geometry("800x500")
    root.configure(fg_color="#f0f0f0")

    heading = ctk.CTkLabel(root, text="Student Face Attendance System", font=("Helvetica", 24, "bold"), text_color="#333")
    heading.pack(pady=30)

    btn_reg = ctk.CTkButton(root, text="Registration", font=("Arial", 16), width=250, height=50, fg_color="#4CAF50", command=open_registration)
    btn_reg.pack(pady=10)

    btn_attend = ctk.CTkButton(root, text="Mark Attendance", font=("Arial", 16), width=250, height=50, fg_color="#2196F3", command=open_mark_attendance)
    btn_attend.pack(pady=10)

    btn_manage_students = ctk.CTkButton(root, text="Student Management", font=("Arial", 16), width=250, height=50, fg_color="#FF9800", command=open_student_mgmt)
    btn_manage_students.pack(pady=10)

    btn_manage_attendance = ctk.CTkButton(root, text="Attendance Management", font=("Arial", 16), width=250, height=50, fg_color="#9C27B0", command=open_attendance_mgmt)
    btn_manage_attendance.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()

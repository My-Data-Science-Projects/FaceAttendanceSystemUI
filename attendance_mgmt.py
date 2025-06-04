import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import date
from database import get_connection

def attendance_management():
    win = ctk.CTkToplevel()
    win.title("Attendance Management")
    win.geometry("1000x600")
    win.lift()
    win.focus_force()
    win.attributes("-topmost", True)
    win.after(100, lambda: win.attributes("-topmost", False))

    top_frame = ctk.CTkFrame(win)
    top_frame.pack(fill="x", pady=10)

    ctk.CTkLabel(top_frame, text="Select Date (YYYY-MM-DD):", font=("Arial", 11)).pack(side="left", padx=10)

    date_var = ctk.StringVar(value=str(date.today()))
    date_entry = ctk.CTkEntry(top_frame, textvariable=date_var, font=("Arial", 11), width=150)
    date_entry.pack(side="left")

    show_btn = ctk.CTkButton(top_frame, text="Show Data", font=("Arial", 10), fg_color="#2196F3", width=100,
                             command=lambda: refresh(date_var.get()))
    show_btn.pack(side="left", padx=10)

    frame = tk.Frame(win, bg="white")
    frame.pack(fill="both", expand=True)

    def refresh(selected_date):
        for widget in frame.winfo_children():
            widget.destroy()

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM attendance WHERE is_delete=0 AND attendance_date=%s", (selected_date,))
            records = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            conn.close()
            return

        conn.close()

        headers = ["Student ID", "Name", "Date", "Time", "Action"]
        for i, text in enumerate(headers):
            label = tk.Label(frame, text=text, font=("Arial", 11, "bold"), bg="#cccccc", fg="black", width=20,
                             borderwidth=1, relief="solid")
            label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        if not records:
            tk.Label(frame, text="No Records Found", font=("Arial", 12, "italic"),
                     fg="gray", bg="white").grid(row=1, column=0, columnspan=5, pady=20)
            return

        for i, record in enumerate(records, start=1):
            for j, value in enumerate(record[1:5]):
                label = tk.Label(frame, text=value, bg="#ffffff", fg="#000000",
                                 font=("Arial", 11), borderwidth=1, relief="solid", width=20)
                label.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)

            action_frame = tk.Frame(frame, bg="#ffffff", borderwidth=1, relief="solid")
            action_frame.grid(row=i, column=4, sticky="nsew", padx=1, pady=1)

            delete_btn = tk.Button(action_frame, text="Delete", bg="#F44336", fg="white",
                                   font=("Arial", 10), width=10,
                                   command=lambda r=record: delete_attendance(r))
            delete_btn.pack(padx=5, pady=5)

    def delete_attendance(record):
        if messagebox.askyesno("Confirm", "Delete attendance record?"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE attendance SET is_delete=1 WHERE id=%s", (record[0],))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Attendance deleted successfully")
            refresh(date_var.get())

    refresh(date_var.get())
import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
import os
import numpy as np
import datetime

# Constants
DATA_DIR = "face_data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# GUI Functions
def register_face():
    name = entry_name.get().strip()
    if not name:
        messagebox.showerror("Input Error", "❌ Please enter a name before registering.")
        return

    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Capturing", "📸 Capturing face. Press 'q' to finish...")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        cv2.imshow("Register - Press 'q' to save", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb)
            encodings = face_recognition.face_encodings(rgb, boxes)

            if encodings:
                np.save(os.path.join(DATA_DIR, f"{name}.npy"), encodings[0])
                messagebox.showinfo("Success", f"✅ Face registered for: {name}")
            else:
                messagebox.showerror("No Face Found", "😕 No face detected. Please try again.")
            break

    cap.release()
    cv2.destroyAllWindows()

def mark_attendance():
    known_faces = []
    known_names = []

    for file in os.listdir(DATA_DIR):
        if file.endswith(".npy"):
            encoding = np.load(os.path.join(DATA_DIR, file))
            known_faces.append(encoding)
            known_names.append(file.split(".")[0])

    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Info", "Scanning faces. Press 'q' to exit...")

    marked = set()
    alerted = set()  # to avoid spamming "unknown" popups

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, boxes)

        if not boxes:
            cv2.imshow("Attendance - Press 'q' to quit", frame)
            if cv2.waitKey(1) == ord('q'):
                break
            continue

        for encode, box in zip(encodings, boxes):
            matches = face_recognition.compare_faces(known_faces, encode)
            name = "Unknown"

            if True in matches:
                idx = matches.index(True)
                name = known_names[idx]

                if name not in marked:
                    with open("attendance.csv", "a") as f:
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        f.write(f"{name},{now}\n")
                    marked.add(name)
                    messagebox.showinfo("Attendance Marked ✅", f"{name}'s attendance recorded at {now}")
            else:
                if str(box) not in alerted:
                    messagebox.showwarning("Unknown Face ❌", "Unrecognized person detected. Please register.")
                    alerted.add(str(box))

            top, right, bottom, left = box
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
            cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,0,0), 2)

        cv2.imshow("Attendance - Press 'q' to quit", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Main GUI Window
root = tk.Tk()
root.title("🧠 AI Face Attendance System")
root.configure(bg="#1e1e2f")
root.state('zoomed')  # Fullscreen on Windows

# Title
title = tk.Label(root, text="Face Attendance System", font=("Arial", 28, "bold"), fg="white", bg="#1e1e2f", pady=20)
title.pack()

# Frame
frame = tk.Frame(root, bg="#2c2c3c", bd=2, relief=tk.GROOVE, padx=30, pady=40)
frame.pack(pady=50)

# Input label + entry
tk.Label(frame, text="Enter Name to Register:", font=("Arial", 16), bg="#2c2c3c", fg="white").pack(pady=(0, 10))
entry_name = tk.Entry(frame, font=("Arial", 16), width=25, bg="#e6e6e6")
entry_name.pack(pady=(0, 20))

# Button style function
def styled_button(master, text, bg, command):
    return tk.Button(master, text=text, font=("Arial", 14, "bold"), fg="white", bg=bg, activebackground="#333333",
                     activeforeground="white", width=20, height=2, command=command, bd=0, relief="raised", cursor="hand2")

# Buttons
styled_button(frame, "📥 Register Face", "#4CAF50", register_face).pack(pady=10)
styled_button(frame, "✅ Mark Attendance", "#2196F3", mark_attendance).pack(pady=10)

# Run App
root.mainloop()

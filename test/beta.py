import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
import os
import numpy as np
import datetime

DATA_DIR = "face_data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def register_face():
    name = entry_name.get().strip()
    if not name:
        messagebox.showerror("Error", "Please enter a name")
        return

    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Info", "Capturing face. Press 'q' to finish...")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        cv2.imshow("Register - Press 'q' to save", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb)
            encodings = face_recognition.face_encodings(rgb, boxes)

            if encodings:
                np.save(os.path.join(DATA_DIR, f"{name}.npy"), encodings[0])
                messagebox.showinfo("Success", f"Face registered for {name}")
            else:
                messagebox.showerror("Error", "No face found. Try again.")
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
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, boxes)

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

            top, right, bottom, left = box
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
            cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,0,0), 2)

        cv2.imshow("Attendance - Press 'q' to quit", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# GUI Layout
root = tk.Tk()
root.title("Face Attendance System")

tk.Label(root, text="Enter Name for Registration").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Button(root, text="Register Face", command=register_face).pack(pady=10)
tk.Button(root, text="Mark Attendance", command=mark_attendance).pack(pady=10)

root.mainloop()

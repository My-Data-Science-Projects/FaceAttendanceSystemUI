import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
import datetime
from face_utils import load_faces
from database import get_connection
from voice_utils import speak_attendance_success

def mark_attendance():
    known_faces, known_names = load_faces()

    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Info", "Press 'q' to stop scanning")

    already_alerted = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding, box in zip(encodings, boxes):
            matches = face_recognition.compare_faces(known_faces, encoding)
            name = "Unknown"

            if True in matches:
                idx = matches.index(True)
                folder_name = known_names[idx]
                name = folder_name.split("_")[0]

                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM student WHERE folder_name = %s", (folder_name,))
                    student_id = cursor.fetchone()[0]

                    now = datetime.datetime.now()

                    cursor.execute("""
                        SELECT COUNT(*) FROM attendance
                        WHERE student_id = %s AND attendance_date = %s AND is_delete = 0
                    """, (student_id, now.strftime("%Y-%m-%d")))
                    already_marked = cursor.fetchone()[0]

                    if already_marked:
                        if student_id not in already_alerted:
                            messagebox.showinfo("Info", f"{name}, your attendance is already marked today.")
                            already_alerted.add(student_id)
                        cap.release()
                        cv2.destroyAllWindows()
                        return
                    else:
                        cursor.execute("""
                            INSERT INTO attendance (student_id, name, attendance_date, attendance_time)
                            VALUES (%s, %s, %s, %s)
                        """, (student_id, name, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")))
                        conn.commit()
                        conn.close()
                        speak_attendance_success(name)
                        messagebox.showinfo("Success", f"Attendance marked for {name}")
                        cap.release()
                        cv2.destroyAllWindows()
                        return

                except Exception as e:
                    messagebox.showerror("DB Error", f"Failed to save attendance: {str(e)}")
                    cap.release()
                    cv2.destroyAllWindows()
                    return
            else:
                name = "Unknown"

            top, right, bottom, left = box
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)

        cv2.imshow("Attendance - Press 'q' to quit", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

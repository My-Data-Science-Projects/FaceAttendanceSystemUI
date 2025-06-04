import cv2
import face_recognition
import numpy as np
import os
import time

def capture_face(folder_path):
    cap = cv2.VideoCapture(0)
    print("Capturing face. Press 'q' to capture...")
    
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
                os.makedirs(folder_path, exist_ok=True)
                np.save(os.path.join(folder_path, "face.npy"), encodings[0])
                print("Face saved successfully.")
            else:
                print("No face found. Try again.")
            break

    cap.release()
    cv2.destroyAllWindows()

def load_faces():
    known_faces = []
    known_names = []

    for folder in os.listdir("face_data"):
        folder_path = os.path.join("face_data", folder)
        face_path = os.path.join(folder_path, "face.npy")
        if os.path.exists(face_path):
            encoding = np.load(face_path)
            known_faces.append(encoding)
            known_names.append(folder)

    return known_faces, known_names
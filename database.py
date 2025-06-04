import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="faceAttendanceDB"
    )

# CREATE TABLE attendance (
# id INT AUTO_INCREMENT PRIMARY KEY,
# student_id INT,
# name VARCHAR(100),
# attendance_date DATE,
# attendance_time TIME,
# is_delete INT DEFAULT 0,
# FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE
# );

# CREATE TABLE student (
# id INT AUTO_INCREMENT PRIMARY KEY,
# name VARCHAR(100),
# course VARCHAR(100),
# admission_date DATE,
# folder_name VARCHAR(150),
# is_delete INT DEFAULT 0
# );
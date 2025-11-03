Student Monthly Billing System
📘 Overview

The Student Monthly Billing System is a simple Python + MySQL desktop application built using Tkinter.
It allows you to view student payment details such as amount, payment date, method, and status — all in an easy-to-read table interface.

⚙️ Features

🔍 Search payment details by student name

💾 Stores data securely in MySQL

📊 Displays data neatly using a Tkinter Treeview table

🚫 Handles invalid inputs and database errors gracefully

🎨 Clean and minimal UI

🧠 Tech Stack
Component	Technology
Language	Python
Database	MySQL
GUI Library	Tkinter
Visualization	ttk Treeview
🗄️ Database Setup
1️⃣ Create Database
CREATE DATABASE Students_database;
USE Students_database;

2️⃣ Create Tables
CREATE TABLE records (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100),
    subject VARCHAR(50),
    marks INT
);

CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    month VARCHAR(20),
    amount DECIMAL(10,2),
    payment_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (student_id) REFERENCES records(student_id)
);

3️⃣ Insert Sample Data
INSERT INTO records (student_name, subject, marks) VALUES
('Ali Khan', 'Mathematics', 85),
('Sara Ahmed', 'Physics', 90),
('Hassan Raza', 'Computer Science', 78),
('Ayesha Noor', 'English', 88),
('Bilal Hussain', 'Chemistry', 92);

INSERT INTO payments (student_id, month, amount, payment_date, status) VALUES
(1, 'January', 5000.00, '2025-01-05', 'Paid'),
(1, 'February', 5000.00, '2025-02-07', 'Paid'),
(2, 'January', 4800.00, '2025-01-10', 'Paid'),
(2, 'February', 4800.00, '2025-02-10', 'Pending'),
(3, 'January', 5200.00, '2025-01-12', 'Late'),
(4, 'January', 5000.00, '2025-01-08', 'Paid'),
(5, 'February', 5300.00, '2025-02-11', 'Pending'),
(5, 'March', 5300.00, '2025-03-05', 'Paid');

💻 How to Run

Install dependencies:

pip install mysql-connector-python


Make sure your MySQL server is running.

Update the MySQL credentials in the Python script:

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="Students_database"
)


Run the program:

python app.py


Enter a student’s name (e.g. Ali Khan) and click “Show Bill”.

📸 Preview

🖥️ Tkinter GUI displaying student payment records in a table format.

🧾 Author

Asad Ullah Khan
Bachelor of Science in Computer Science (BSCS) — FUUAST
📍 Karachi, Pakistan

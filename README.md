📚 Student Management System (Python + MySQL)

A complete Student Management System built using Python and MySQL.
This program allows you to perform all CRUD operations:

✔ Add Student
✔ Update Student
✔ Delete Student
✔ View All Students
✔ Search by ID
✔ Auto-create database & table
✔ Add sample data
✔ Works with XAMPP / MySQL Server


---

🚀 Features

🔧 Automatic Database Setup

Checks if the database student_management exists

If not, it creates the database & students table automatically


🎯 CRUD Operations

Add new student

Edit existing student information

Delete student record

View all students

Search student by ID


🧪 Sample Data

Automatically inserts 5 sample students (only if table is empty)


🛡️ Error Handling

Validates user input

Handles MySQL exceptions

Prevents invalid operations



---

🗂️ Table Structure

The students table contains:

Column	Type	Description

id	INT (PK)	Auto Increment
name	VARCHAR(100)	Student Name
age	INT	Student Age
class	VARCHAR(50)	Class/Section
marks	DECIMAL(5,2)	Student Marks
created_at	TIMESTAMP	Auto Timestamp



---

🛠️ Requirements

Python 3.x

MySQL / XAMPP

mysql-connector-python library


Install the connector:

pip install mysql-connector-python


---

▶️ How to Run

1. Ensure XAMPP MySQL server is running


2. Save the Python script as student_management.py


3. Run the script:



python student_management.py

The program will automatically:

✔ Create the database (if missing)
✔ Create the table
✔ Insert sample data (if empty)
✔ Show menu options


---

🖥️ Menu Options

1. Add New Student
2. Update Student
3. Delete Student
4. View All Students
5. Search Student by ID
6. Add Sample Data
7. Exit


---

📌 Example Outputs

Adding a Student

Enter Name: John
Enter Age: 21
Enter Class: CS-A
Enter Marks: 88.5

✅ Student 'John' added successfully!

Viewing Students

ID   Name                Age   Class     Marks    Created
1    John Doe            20    CS-A      85.50    2025-01-12


---

📦 Project Flow

Initialize Database → Create table → Add Sample Data → Show Menu → Perform CRUD Operations


---

📄 Code Structure

student_management.py
├── get_connection()
├── initialize_database()
├── add_student()
├── update_student()
├── delete_student()
├── view_students()
├── search_by_id()
├── add_sample_data()
└── display_menu()


---
📜 License

This project is completely free to use and modify.


---


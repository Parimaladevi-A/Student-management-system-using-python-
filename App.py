import mysql.connector
from mysql.connector import Error

# Database Connection
def get_connection():
    try:
        # First try to connect with the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="student_management",
            auth_plugin='mysql_native_password'
        )
        return conn
    except Error as e:
        if "Unknown database" in str(e):
            # Database doesn't exist, create it
            print("Database 'student_management' not found. Creating it...")
            try:
                # Connect without specifying database
                temp_conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    auth_plugin='mysql_native_password'
                )
                temp_cursor = temp_conn.cursor()
                
                # Create database
                temp_cursor.execute("CREATE DATABASE student_management")
                print("✅ Database 'student_management' created successfully!")
                
                # Create table
                temp_cursor.execute("USE student_management")
                create_table_query = """
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INT NOT NULL,
                    class VARCHAR(50) NOT NULL,
                    marks DECIMAL(5,2) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                temp_cursor.execute(create_table_query)
                temp_conn.commit()
                
                temp_cursor.close()
                temp_conn.close()
                
                # Now connect with the database
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="student_management",
                    auth_plugin='mysql_native_password'
                )
                print("✅ Connected to student_management database!")
                return conn
                
            except Error as create_error:
                print(f"❌ Error creating database: {create_error}")
                return None
        else:
            print(f"❌ Connection error: {e}")
            return None

def initialize_database():
    """Initialize database and table on first run"""
    print("🔧 INITIALIZING DATABASE...")
    print("-" * 40)
    
    conn = get_connection()
    if conn:
        print("✅ Database setup complete!")
        conn.close()
    else:
        print("❌ Failed to initialize database")
        exit(1)

# Add Student 
def add_student():
    print("\n" + "="*40)
    print(" ADD STUDENT")
    print("="*40)
    
    try:
        name = input("Enter Name: ").strip()
        if not name:
            print("❌ Name cannot be empty")
            return
        
        age_input = input("Enter Age: ").strip()
        if not age_input.isdigit():
            print("❌ Age must be a number")
            return
        age = int(age_input)
        
        student_class = input("Enter Class: ").strip()
        if not student_class:
            print("❌ Class cannot be empty")
            return
        
        marks_input = input("Enter Marks: ").strip()
        try:
            marks = float(marks_input)
        except ValueError:
            print("❌ Marks must be a number")
            return

        conn = get_connection()
        if not conn:
            print("❌ Cannot connect to database")
            return
        
        cur = conn.cursor()
        query = "INSERT INTO students (name, age, class, marks) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (name, age, student_class, marks))
        conn.commit()
        
        print(f"✅ Student '{name}' added successfully!")
        print(f"   ID: {cur.lastrowid}, Age: {age}, Class: {student_class}, Marks: {marks}")
        
        cur.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Update Student 
def update_student():
    print("\n" + "="*40)
    print(" UPDATE STUDENT")
    print("="*40)
    
    try:
        student_id_input = input("Enter Student ID: ").strip()
        if not student_id_input.isdigit():
            print("❌ Student ID must be a number")
            return
        student_id = int(student_id_input)

        # First check if student exists
        conn = get_connection()
        if not conn:
            print("❌ Cannot connect to database")
            return
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cur.fetchone()
        
        if not student:
            print(f"❌ No student found with ID {student_id}")
            conn.close()
            return
        
        print(f"\nCurrent details for Student ID {student_id}:")
        print(f"  Name: {student[1]}")
        print(f"  Age: {student[2]}")
        print(f"  Class: {student[3]}")
        print(f"  Marks: {student[4]}")
        
        print("\nEnter new values (leave blank to keep current):")

        name = input(f"New Name [{student[1]}]: ").strip()
        age_input = input(f"New Age [{student[2]}]: ").strip()
        class_new = input(f"New Class [{student[3]}]: ").strip()
        marks_input = input(f"New Marks [{student[4]}]: ").strip()

        # Prepare update query
        updates = []
        values = []
        
        if name:
            updates.append("name = %s")
            values.append(name)
        
        if age_input:
            if age_input.isdigit():
                updates.append("age = %s")
                values.append(int(age_input))
            else:
                print("❌ Age must be a number")
                conn.close()
                return
        
        if class_new:
            updates.append("class = %s")
            values.append(class_new)
        
        if marks_input:
            try:
                updates.append("marks = %s")
                values.append(float(marks_input))
            except ValueError:
                print("❌ Marks must be a number")
                conn.close()
                return

        if not updates:
            print("⚠️ No changes made")
            conn.close()
            return

        # Add student_id to values
        values.append(student_id)
        
        query = f"UPDATE students SET {', '.join(updates)} WHERE id = %s"
        cur.execute(query, values)
        conn.commit()
        
        print(f"✅ Student ID {student_id} updated successfully!")
        
        cur.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Delete Student 
def delete_student():
    print("\n" + "="*40)
    print(" DELETE STUDENT")
    print("="*40)
    
    try:
        student_id_input = input("Enter Student ID to Delete: ").strip()
        if not student_id_input.isdigit():
            print("❌ Student ID must be a number")
            return
        student_id = int(student_id_input)

        # First check if student exists
        conn = get_connection()
        if not conn:
            print("❌ Cannot connect to database")
            return
        
        cur = conn.cursor()
        cur.execute("SELECT name FROM students WHERE id = %s", (student_id,))
        student = cur.fetchone()
        
        if not student:
            print(f"❌ No student found with ID {student_id}")
            conn.close()
            return
        
        print(f"\n⚠️ You are about to delete:")
        print(f"   Student ID: {student_id}")
        print(f"   Name: {student[0]}")
        
        confirm = input("\nAre you sure? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
            conn.commit()
            print(f"✅ Student '{student[0]}' deleted successfully!")
        else:
            print("❌ Deletion cancelled")
        
        cur.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

# View All Students
def view_students():
    print("\n" + "="*60)
    print(" ALL STUDENTS")
    print("="*60)
    
    try:
        conn = get_connection()
        if not conn:
            print("❌ Cannot connect to database")
            return
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM students ORDER BY id")
        rows = cur.fetchall()
        
        if not rows:
            print("📭 No students found in the database")
        else:
            print(f"📊 Total Students: {len(rows)}")
            print("-" * 60)
            print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Class':<10} {'Marks':<8} {'Created'}")
            print("-" * 60)
            
            for row in rows:
                # Format created_at date
                created_date = row[5].strftime('%Y-%m-%d') if row[5] else 'N/A'
                print(f"{row[0]:<5} {row[1]:<20} {row[2]:<5} {row[3]:<10} {row[4]:<8.2f} {created_date}")
        
        cur.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Search by ID 
def search_by_id():
    print("\n" + "="*40)
    print(" SEARCH STUDENT BY ID")
    print("="*40)
    
    try:
        student_id_input = input("Enter Student ID: ").strip()
        if not student_id_input.isdigit():
            print("❌ Student ID must be a number")
            return
        student_id = int(student_id_input)

        conn = get_connection()
        if not conn:
            print("❌ Cannot connect to database")
            return
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        row = cur.fetchone()
        
        if row:
            print(f"\n✅ Student Found:")
            print("-" * 40)
            print(f"ID:      {row[0]}")
            print(f"Name:    {row[1]}")
            print(f"Age:     {row[2]}")
            print(f"Class:   {row[3]}")
            print(f"Marks:   {row[4]:.2f}")
            print(f"Created: {row[5].strftime('%Y-%m-%d %H:%M:%S') if row[5] else 'N/A'}")
        else:
            print(f"❌ No student found with ID {student_id}")
        
        cur.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Add some sample students
def add_sample_data():
    """Add sample students for testing"""
    try:
        conn = get_connection()
        if not conn:
            return
        
        cur = conn.cursor()
        
        # Check if table is empty
        cur.execute("SELECT COUNT(*) FROM students")
        count = cur.fetchone()[0]
        
        if count == 0:
            print("\n📝 Adding sample students...")
            sample_students = [
                ("John Doe", 20, "CS-A", 85.5),
                ("Jane Smith", 21, "CS-B", 92.0),
                ("Bob Johnson", 19, "IT-A", 78.5),
                ("Alice Brown", 22, "IT-B", 88.0),
                ("Charlie Wilson", 20, "CS-A", 91.5)
            ]
            
            query = "INSERT INTO students (name, age, class, marks) VALUES (%s, %s, %s, %s)"
            for student in sample_students:
                cur.execute(query, student)
            
            conn.commit()
            print("✅ Added 5 sample students!")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Note: {e}")

# Display menu
def display_menu():
    print("\n" + "="*60)
    print(" STUDENT MANAGEMENT SYSTEM")
    print("="*60)
    print("1. Add New Student")
    print("2. Update Student")
    print("3. Delete Student")
    print("4. View All Students")
    print("5. Search Student by ID")
    print("6. Add Sample Data")
    print("7. Exit")
    print("-" * 60)

# Main Program
if __name__ == "__main__":
    print("\n" + "="*70)
    print(" STUDENT MANAGEMENT SYSTEM")
    print(" MySQL DATABASE (XAMPP)")
    print("="*70)
    
    # Initialize database on startup
    initialize_database()
    
    # Add sample data if empty
    add_sample_data()
    
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                add_student()
            elif choice == "2":
                update_student()
            elif choice == "3":
                delete_student()
            elif choice == "4":
                view_students()
            elif choice == "5":
                search_by_id()
            elif choice == "6":
                add_sample_data()
            elif choice == "7":
                print("\n👋 Thank you for using Student Management System!")
                print("Goodbye! 🎓")
                break
            else:
                print("❌ Invalid Option! Please enter 1-7")
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Program interrupted by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()

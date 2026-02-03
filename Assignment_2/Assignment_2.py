import sqlite3

#reusable variables
DB_FILE = "students.db"

def connect_db():
    return sqlite3.connect(DB_FILE)

def setup_table():
    database = connect_db() # open database file

    #make sure students table exists in db
    database.execute("""CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT NOT NULL, grade TEXT NOT NULL, email TEXT NOT NULL);""")

    database.commit() # save changes to db
    database.close() # close database

#back end functions
def add_student(name, grade, email): # function for adding students to the database
    database = connect_db()

    #inserts data into the db
    database.execute("INSERT INTO students (name, grade, email) VALUES (?, ?, ?)", (name, grade, email))

    #save and exits updated db
    database.commit() 
    database.close() 

def view_students_db(): #function for viewing students within the databse
    database = connect_db()

    #create a cursor to grab students records in the db
    cursor = database.execute("SELECT id, name, grade, email FROM students")

    #saves the database object as rows
    rows = cursor.fetchall()

    #print the database one row at a time
    for row in rows: 
        print(row)

    database.close()

def update_student(student_id, name, grade, email):
    database = connect_db()
    database.execute(
        "UPDATE students SET name = ?, grade = ?, email = ? WHERE id = ?",
        (name, grade, email, student_id)
    )
    database.commit()
    database.close()

def delete_student(student_id):
    database = connect_db()
    database.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )
    database.commit()
    database.close()


#user interface functions
def print_menu(): 
    print("\n--- Student Database Menu ---")
    print("1) Add students")
    print("2) View students")
    print("3) Update students")
    print("4) Delete Students")
    print("5) Exit")

def user_choice():
    choice = input("Choose an option (1-5): ").strip()
    return choice

def main():
    setup_table()

    done = False #flag variable for flow control
    while not done: 
        print_menu()
        choice = user_choice()

        if choice == "1":
            name = input("Name: ").strip()
            grade = input("Grade: ").strip()
            email = input("Email: ").strip()
            add_student(name, grade, email)
            print("Student Added")
        
        elif choice == "2":
            view_students_db()
        
        elif choice == "3": 
            try: 
                student_id = int(input("Student ID to update: ").strip())
                name = input("New name: ").strip()
                grade = input("New grade: ").strip()
                email = input("New email: ").strip()

                update_student(student_id, name, grade, email)
                print("Student updated.")

            except ValueError: 
                print("Invalid ID. Must be a number.")

        elif choice == "4": 
            try:
                student_id = int(input("Student ID to delete: ").strip())
                confirm = input(f"Delete student {student_id}? (y/n): ").strip().lower()

                if confirm == "y":
                    delete_student(student_id)
                    print("Student deleted.")
                else:
                    print("Delete canceled.")

            except ValueError:
                print("Invalid ID. Must be a number.")

        elif choice == "5": 
            done = True
            print("Exiting Program...")

        else: 
            print("Invalid input, Try again.")







if __name__ == "__main__":
    main()
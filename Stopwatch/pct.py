

import tkinter as tk
from tkinter import messagebox, Listbox, END
import sqlite3

# Setup database connection
def setup_database():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            marks REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a student
def add_student():
    student_id = int(entry_id.get())
    name = entry_name.get()
    age = entry_age.get()
    marks = entry_marks.get()

    if not student_id or not name or not age or not marks:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    try:
        age = int(age)
        marks = float(marks)
    except ValueError:
        messagebox.showerror("Input Error", "Age must be an integer and Marks must be a number.")
        return

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (id, name, age, marks) VALUES (?, ?, ?, ?)", 
                   (student_id, name, age, marks))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student added successfully. You can add more students.")
    display_students()  # Refresh the list


# Function to update a student
def update_student():
    student_id = int(entry_id.get())
    name = entry_name.get()
    age = entry_age.get()
    marks = entry_marks.get()

    if not student_id:
        messagebox.showerror("Input Error", "Student ID is required.")
        return

    try:
        age = int(age)
        marks = float(marks)
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET name=?, age=?, marks=? WHERE id=?", 
                       (name, age, marks, student_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student updated successfully.")
        display_students()  # Refresh the list
    except sqlite3.Error:
        messagebox.showerror("Database Error", "Could not update the student. Please check the ID.")
        return


# Function to delete a student
def delete_student():
    student_id = entry_id.get()

    if not student_id:
        messagebox.showerror("Input Error", "Student ID is required.")
        return

    try:
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student deleted successfully.")
        display_students()  # Refresh the list
    except sqlite3.Error:
        messagebox.showerror("Database Error", "Could not delete the student. Please check the ID.")
        return


# Function to display students
def display_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    conn.close()

    if not records:
        messagebox.showinfo("Info", "No students found.")
        return
    listbox.delete(0, END)  # Clear the listbox
    for record in records:
        listbox.insert(END, f"ID: {record[0]}, Name: {record[1]}, Age: {record[2]}, Marks: {record[3]}")

# Create the main window
root = tk.Tk()
root.title("Student Management System")

# Create entry fields
tk.Label(root, text="Student ID").grid(row=0, column=0)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1)

tk.Label(root, text="Name").grid(row=1, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1)

tk.Label(root, text="Age").grid(row=2, column=0)
entry_age = tk.Entry(root)
entry_age.grid(row=2, column=1)

tk.Label(root, text="Marks").grid(row=3, column=0)
entry_marks = tk.Entry(root)
entry_marks.grid(row=3, column=1)

# Create buttons
tk.Button(root, text="Add", command=add_student).grid(row=4, column=0)
tk.Button(root, text="Update", command=update_student).grid(row=4, column=1)
tk.Button(root, text="Delete", command=delete_student).grid(row=4, column=2)
tk.Button(root, text="Display", command=display_students).grid(row=4, column=3)

# Create Listbox to display students
scrollbar = tk.Scrollbar(root)  # Create a scrollbar
scrollbar.grid(row=5, column=4, sticky='ns')  # Position the scrollbar

listbox = Listbox(root, font=("Helvetica", 14), height=10, width=50)  # Set a larger font size and dimensions
listbox.grid(row=5, column=0, columnspan=4)  # Adjust grid position

listbox.config(yscrollcommand=scrollbar.set)  # Link scrollbar to listbox
scrollbar.config(command=listbox.yview)  # Link listbox to scrollbar


listbox.grid(row=5, column=0, columnspan=4)

# Setup the database
setup_database()

# Run the application
root.mainloop()




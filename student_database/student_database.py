import tkinter as tk
import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import sys

# Create a new SQLite database
conn = sqlite3.connect('data//students_information_system.db')
mycursor = conn.cursor()


def load_data():
    # Clear the existing table
    for row in tree.get_children():
        tree.delete(row)

    # Fetch the data from the database
    mycursor.execute("SELECT * FROM students")
    data = mycursor.fetchall()

    # Populate the table with the data
    for row in data:
        tree.insert("", "end", values=row)

def add_student():
    # Get the student attributes from the entry fields
    student_number = student_number_entry.get()
    name = name_entry.get()
    birthday = birthday_entry.get()
    email = email_entry.get()
    contact_number = contact_number_entry.get()


  # Validate the input fields
    if not (student_number.isdigit() and len(student_number) == 10):
        messagebox.showerror("Error", "Invalid student number. Please enter a 10-digit number.")
        return
    
    if not all(letter.isalpha() or letter.isspace() for letter in name):
        messagebox.showerror("Error", "Invalid name. Please enter your name.")
        return


    if not (len(birthday) == 10 and birthday[4] == "-" and birthday[7] == "-" and birthday[:4].isdigit() and birthday[5:7].isdigit() and birthday[8:].isdigit()):
        messagebox.showerror("Error", "Invalid birthday. Please enter a valid date in the format YYYY-MM-DD.")
        return

    if not ("@" in email and "." in email):
        messagebox.showerror("Error", "Invalid email. Please enter a valid email address.")
        return

    if not (contact_number.isdigit() and len(contact_number) == 12):
        messagebox.showerror("Error", "Invalid contact number. Please enter an 12-digit number.")
        return
    
    # Insert the student into the database
    sql = "INSERT INTO students (student_number, name, birthday, email, contact_number) VALUES (?, ?, ?, ?, ?   )"
    val = (student_number, name, birthday, email, contact_number)
    mycursor.execute(sql, val)
    conn.commit()
    messagebox.showinfo("Success!", "Student added successfully!")



    # Clear the entry fields
    student_number_entry.delete(0, END)
    name_entry.delete(0, END)
    birthday_entry.delete(0, END)
    email_entry.delete(0, END)
    contact_number_entry.delete(0, END)
    load_data()


# Create a function to search for a student in the database
def search_student():
    # Get the student number from the entry field
    student_number = student_number_entry.get()
    
    # Validate the input field
    if not (student_number.isdigit() and len(student_number) == 10):
        messagebox.showerror("Error", "Invalid student number. Please enter a 10-digit number.")
        return


    # Search for the student in the database
    sql = "SELECT * FROM students WHERE student_number = ?"
    val = (student_number,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    # If the student is found, display their information
    if result:
        name_entry.delete(0, END)
        name_entry.insert(0, result[1])
        birthday_entry.delete(0, END)
        birthday_entry.insert(0, result[2])
        email_entry.delete(0, END)
        email_entry.insert(0, result[3])
        contact_number_entry.delete(0, END)
        contact_number_entry.insert(0, result[4])
        messagebox.showinfo("Success!", "Student found!")
        load_data()

    else:
        # Clear the entry fields and update the status label to indicate failure
        name_entry.delete(0, END)
        birthday_entry.delete(0, END)
        email_entry.delete(0, END)
        contact_number_entry.delete(0, END)
        messagebox.showerror("Student not found!")

# Create a function to update a student's information in the database
def update_student():
    # Get the student attributes from the entry fields
    student_number = student_number_entry.get()
    name = name_entry.get()
    birthday = birthday_entry.get()
    email = email_entry.get()
    contact_number = contact_number_entry.get()
    
    # Validate the input field
    if not (student_number.isdigit() and len(student_number) == 10):
        messagebox.showerror("Error", "Invalid student number. Please enter a 10-digit number.")
        return

    # Update the student in the database
    sql = "UPDATE students SET name = ?, birthday = ?, email = ?, contact_number = ? WHERE student_number = ?"
    val = (name, birthday, email, contact_number, student_number)
    mycursor.execute(sql, val)
    conn.commit()
    messagebox.showinfo("Success!","Student data updated successfully!")
    load_data()

# Create a function to delete a student from the database
def delete_student():
    # Get the student number from the entry field
    student_number = student_number_entry.get()

    # Validate the input field
    if not (student_number.isdigit() and len(student_number) == 10):
        messagebox.showerror("Error", "Invalid student number. Please enter a 10-digit number.")
        return

    # Delete the student from the database
    sql = "DELETE FROM students WHERE student_number = ?"
    val = (student_number,)
    mycursor.execute(sql, val)
    conn.commit()

    # Clear the entry fields and update the status label to indicate success
    name_entry.delete(0, END)
    birthday_entry.delete(0, END)
    email_entry.delete(0, END)
    contact_number_entry.delete(0, END)
    messagebox.showinfo("Success!", "Student data is successfully deleted!")
    load_data()



# Create the GUI
root = Tk()
root.title("Student Information System")
root.geometry("1120x250")

# Make the window unresizable
root.resizable(False, False)

# Create the entry fields

# Student Number
student_number_label = Label(root, text="Student Number")
student_number_label.grid(row=2, column=0, columnspan=5, pady=2, padx=10)
student_number_entry = Entry(root)
student_number_entry.grid(row=2, column=6, columnspan=5, pady=2)

# Student Name
name_label = Label(root, text="Name")
name_label.grid(row=3, column=0, columnspan=5, pady=2, padx=5)
name_entry = Entry(root)
name_entry.grid(row=3, column=6, columnspan=5, pady=2)

# Student Birthday
birthday_label = Label(root, text="Birthday")
birthday_label.grid(row=4, column=0, columnspan=5, pady=2, padx=5)
birthday_entry = Entry(root)
birthday_entry.grid(row=4, column=6, columnspan=5, pady=2)

# Student Email
email_label = Label(root, text="Email")
email_label.grid(row=5, column=0, columnspan=5, pady=2, padx=5)
email_entry = Entry(root)
email_entry.grid(row=5, column=6, columnspan=5, pady=2)

# Student Contact Number
contact_number_label = Label(root, text="Contact Number")
contact_number_label.grid(row=6, column=0, columnspan=5, pady=2, padx=5)
contact_number_entry = Entry(root)
contact_number_entry.grid(row=6, column=6, columnspan=5, pady=2)

# Create the buttons
add_button = Button(root, text="Submit Student Information to Database", command=add_student)
add_button.grid(row=7, column=0, padx=10, pady=3, ipadx=23, columnspan=12)

search_button = Button(root, text="Search", command=search_student)
search_button.grid(row=8, column=0, pady=8, ipadx=15, columnspan=4)

update_button = Button(root, text="Update", command=update_student)
update_button.grid(row=8, column=4, pady=8, ipadx=16, columnspan=4)

delete_button = Button(root, text="Delete", command=delete_student)
delete_button.grid(row=8, column=8, pady=8, ipadx=17, columnspan=4)

status_label = Label(root, text="")
status_label.grid(row=7, column=0, columnspan=2)

tree = ttk.Treeview(root, show='headings', columns=("student_number","name","birthday","email","contact_number"))
tree.heading("student_number", text="Student Number")
tree.heading("name", text="Name")
tree.heading("birthday", text="Birthday")
tree.heading("email", text="Email")
tree.heading("contact_number", text="Contact Number")
tree.column("birthday", width=150)
tree.column("student_number", width=150)
tree.column("contact_number", width=150)
tree.column("name", width=150)
tree.grid(row=2, column=12, rowspan = 7, pady=10, padx=10)

sql = "SELECT * FROM students"
mycursor.execute(sql)
results = mycursor.fetchall()
for result in results:
    tree.insert("", "end", text=result[4], values=(result[0], result[1], result[2], result[3], result[4]))
    print(result)

# Run the GUI
root.mainloop()
conn.close()
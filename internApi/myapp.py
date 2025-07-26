# import requests
# URL = "http://127.0.0.1:8000/stuinfo/"

# req = requests.get(url = URL)
# data = req.json()
# print(data)  # This will print the JSON response from the API

# this is the seperate application to calling the API's
# This code snippet is used to fetch and print student information from the API.
# It uses the requests library to make a GET request to the specified URL and prints the JSON response.

# if calling the any api into this file then call it into this file
# This code snippet is used to fetch and print student information from the API.
# It uses the requests library to make a GET request to the specified URL and prints the JSON

import requests
import tkinter as tk
from tkinter import ttk

# API URL
# URL = "http://127.0.0.1:8000/api/students/"  # Ensure this is the correct API endpoint
URL = "http://127.0.0.1:8000/stuinfo/"


# Fetch data from API
def fetch_data():
    try:
        response = requests.get(URL)
        data = response.json()
        return data
    except Exception as e:
        print("Error fetching data:", e)
        return []

# Create GUI Window
root = tk.Tk()
root.title("Student Info Table")
root.geometry("600x400")

# Treeview Table
tree = ttk.Treeview(root)
tree["columns"] = ("ID","Name", "Roll No", "City")

tree.column("#0", width=0, stretch=tk.NO)  # Hide first column
tree.column("Name", anchor=tk.W, width=200)
tree.column("Roll No", anchor=tk.CENTER, width=100)
tree.column("City", anchor=tk.W, width=200)

tree.heading("ID", text="ID", anchor=tk.W)
tree.heading("Name", text="Name", anchor=tk.W)
tree.heading("Roll No", text="Roll No", anchor=tk.CENTER)
tree.heading("City", text="City", anchor=tk.W)

tree.pack(fill=tk.BOTH, expand=True)

# Load data into table
student_data = fetch_data()
for student in student_data:
    tree.insert("", tk.END, values=(student['id'],student['name'], student['roll'], student['city']))

# Run GUI
root.mainloop()
# response from the API
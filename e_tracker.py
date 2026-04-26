# EXPENSE TRACKER

import tkinter as tk
from tkinter import messagebox, ttk
import json
import matplotlib.pyplot as plt
from datetime import datetime


USERS_FILE = "users.json"
EXPENSE_FILE = "expenses.json"


def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)


def load_expenses():
    try:
        with open(EXPENSE_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_expenses(data):
    with open(EXPENSE_FILE, "w") as f:
        json.dump(data, f)

# GLOBAL DATA
users = load_users()
expenses = load_expenses()
current_user = None

# LOGIN / REGISTER
def register():
    username = user_entry.get()
    password = pass_entry.get()

    if username in users:
        messagebox.showerror("Error", "User already exists")
        return

    users[username] = password
    save_users(users)
    messagebox.showinfo("Success", "Registered Successfully")

def login():
    global current_user
    username = user_entry.get()
    password = pass_entry.get()

    if username in users and users[username] == password:
        current_user = username
        root.destroy()
        open_dashboard()
    else:
        messagebox.showerror("Error", "Invalid Credentials")

# DASHBOARD
def open_dashboard():
    global tree

    dash = tk.Tk()
    dash.title("Expense Dashboard")
    dash.geometry("700x600")

    tk.Label(dash, text=f"Welcome {current_user}", font=("Arial", 14)).pack()

    # INPUTS
    tk.Label(dash, text="Amount").pack()
    amount_entry = tk.Entry(dash)
    amount_entry.pack()

    tk.Label(dash, text="Category").pack()
    category_var = tk.StringVar()
    category_menu = tk.OptionMenu(dash, category_var, "Food", "Transport", "Rent", "Shopping", "Other")
    category_menu.pack()

    tk.Label(dash, text="Date (YYYY-MM-DD)").pack()
    date_entry = tk.Entry(dash)
    date_entry.pack()

    # FUNCTIONS
    def add_expense():
        try:
            amount = float(amount_entry.get())
            category = category_var.get()
            date = date_entry.get()

            datetime.strptime(date, "%Y-%m-%d")

            exp = {"amount": amount, "category": category, "date": date, "user": current_user}
            expenses.append(exp)
            save_expenses(expenses)

            tree.insert("", tk.END, values=(amount, category, date))

            amount_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)

        except:
            messagebox.showerror("Error", "Invalid input")

    def delete_expense():
        selected = tree.selection()
        for item in selected:
            index = tree.index(item)
            tree.delete(item)
            expenses.pop(index)
        save_expenses(expenses)

    def show_total():
        total = sum(e["amount"] for e in expenses if e["user"] == current_user)
        messagebox.showinfo("Total", f"Rs. {total}")

    def show_chart():
        data = {}
        for e in expenses:
            if e["user"] == current_user:
                data[e["category"]] = data.get(e["category"], 0) + e["amount"]

        plt.bar(data.keys(), data.values())
        plt.title("Expenses by Category")
        plt.show()

    def filter_month():
        month = month_entry.get()
        tree.delete(*tree.get_children())
        for e in expenses:
            if e["user"] == current_user and e["date"].startswith(month):
                tree.insert("", tk.END, values=(e["amount"], e["category"], e["date"]))

    # BUTTONS
    tk.Button(dash, text="Add", command=add_expense).pack()
    tk.Button(dash, text="Delete", command=delete_expense).pack()
    tk.Button(dash, text="Total", command=show_total).pack()
    tk.Button(dash, text="Chart", command=show_chart).pack()

    # FILTER
    tk.Label(dash, text="Filter by Month (YYYY-MM)").pack()
    month_entry = tk.Entry(dash)
    month_entry.pack()
    tk.Button(dash, text="Apply Filter", command=filter_month).pack()

    # TABLE
    columns = ("Amount", "Category", "Date")
    tree = ttk.Treeview(dash, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)

    tree.pack(fill=tk.BOTH, expand=True)

    # LOAD DATA
    for e in expenses:
        if e["user"] == current_user:
            tree.insert("", tk.END, values=(e["amount"], e["category"], e["date"]))

    dash.mainloop()


# LOGIN UI
root = tk.Tk()
root.title("Login")
root.geometry("300x250")


tk.Label(root, text="Username").pack()
user_entry = tk.Entry(root)
user_entry.pack()


tk.Label(root, text="Password").pack()
pass_entry = tk.Entry(root, show="*")
pass_entry.pack()


tk.Button(root, text="Login", command=login).pack(pady=5)

tk.Button(root, text="Register", command=register).pack(pady=5)

root.mainloop()
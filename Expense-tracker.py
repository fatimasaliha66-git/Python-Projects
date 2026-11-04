import tkinter as tk
from tkinter import ttk, messagebox
import json

# Functions
def add_expense():
    amount = amount_entry.get()
    category = category_combobox.get()
    if not amount.isdigit():
        messagebox.showerror("Invalid Input", "Amount must be a number.")
        return
    if not category:
        messagebox.showerror("Invalid Input", "Please select a category.")
        return
    expense = {'amount': float(amount), 'category': category}
    expenses.append(expense)
    update_expense_list()
    messagebox.showinfo("Success", "Expense added successfully!")
    amount_entry.delete(0, tk.END)

def update_expense_list():
    expense_listbox.delete(0, tk.END)
    for i, expense in enumerate(expenses, start=1):
        expense_listbox.insert(tk.END, f"{i}. {expense['category']}: ${expense['amount']:.2f}")

def remove_expense():
    selected = expense_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Please select an expense to remove.")
        return
    index = selected[0]
    expenses.pop(index)
    update_expense_list()
    messagebox.showinfo("Success", "Expense removed successfully!")

def calculate_total_expenses():
    total = sum(expense['amount'] for expense in expenses)
    messagebox.showinfo("Total Expenses", f"Your total expenses are: ${total:.2f}")

def save_expenses():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file)
    messagebox.showinfo("Success", "Expenses saved successfully!")

def load_expenses():
    global expenses
    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
        update_expense_list()
        messagebox.showinfo("Success", "Expenses loaded successfully!")
    except FileNotFoundError:
        messagebox.showerror("Error", "No saved expenses found.")

def clear_all_expenses():
    global expenses
    expenses = []
    update_expense_list()
    messagebox.showinfo("Success", "All expenses cleared.")

# Main Window
root = tk.Tk()
root.title("Expense Tracker")

# Add Expense Frame
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Amount:").grid(row=0, column=0)
amount_entry = ttk.Entry(frame)
amount_entry.grid(row=0, column=1)

ttk.Label(frame, text="Category:").grid(row=1, column=0)
category_combobox = ttk.Combobox(frame, values=["Food", "Transport", "Shopping", "Entertainment", "Other"])
category_combobox.grid(row=1, column=1)

ttk.Button(frame, text="Add Expense", command=add_expense).grid(row=2, column=0, columnspan=2)

# View Expenses Frame
view_frame = ttk.Frame(root, padding="10")
view_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))

ttk.Label(view_frame, text="Expenses:").grid(row=0, column=0, sticky=tk.W)
expense_listbox = tk.Listbox(view_frame, height=10, width=50)
expense_listbox.grid(row=1, column=0, columnspan=2)

ttk.Button(view_frame, text="Remove Expense", command=remove_expense).grid(row=2, column=0)
ttk.Button(view_frame, text="Clear All", command=clear_all_expenses).grid(row=2, column=1)

# Summary Frame
summary_frame = ttk.Frame(root, padding="10")
summary_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))

ttk.Button(summary_frame, text="Calculate Total", command=calculate_total_expenses).grid(row=0, column=0)
ttk.Button(summary_frame, text="Save Expenses", command=save_expenses).grid(row=0, column=1)
ttk.Button(summary_frame, text="Load Expenses", command=load_expenses).grid(row=0, column=2)

# Initialize Expense List
expenses = []

# Run App
root.mainloop()

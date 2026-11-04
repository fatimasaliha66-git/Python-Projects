import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class JournalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Journal App")

        self.entries = []

        # GUI Components
        self.create_widgets()
        self.load_entries()

    def create_widgets(self):
        # Date Input
        self.date_label = ttk.Label(self.root, text="Date (YYYY-MM-DD):")
        self.date_label.pack(pady=5)
        self.date_entry = ttk.Entry(self.root, width=20)
        self.date_entry.pack(pady=5)

        # Content Input
        self.content_label = ttk.Label(self.root, text="Journal Entry:")
        self.content_label.pack(pady=5)
        self.content_text = tk.Text(self.root, height=10, width=40)
        self.content_text.pack(pady=5)

        # Buttons
        self.add_button = ttk.Button(self.root, text="Add Entry", command=self.add_entry)
        self.add_button.pack(pady=5)

        self.delete_button = ttk.Button(self.root, text="Delete Entry", command=self.delete_entry)
        self.delete_button.pack(pady=5)

        self.view_button = ttk.Button(self.root, text="View Entries", command=self.view_entries)
        self.view_button.pack(pady=5)

        self.search_button = ttk.Button(self.root, text="Search Entries", command=self.search_entries)
        self.search_button.pack(pady=5)

        self.list_button = ttk.Button(self.root, text="List All Entries", command=self.list_entries)
        self.list_button.pack(pady=5)

        # Output area for search results
        self.output_text = ttk.Label(self.root, text="", justify="left")
        self.output_text.pack(pady=5)

    def add_entry(self):
        date = self.date_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()

        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        if not content:
            messagebox.showerror("Error", "Entry content cannot be empty.")
            return

        entry = {'date': date, 'content': content}
        self.entries.append(entry)
        self.save_entries()
        self.clear_entries()
        messagebox.showinfo("Success", "Entry added successfully!")

    def delete_entry(self):
        date = self.date_entry.get()
        if not date:
            messagebox.showerror("Error", "Please enter a date to delete an entry.")
            return

        for entry in self.entries:
            if entry['date'] == date:
                self.entries.remove(entry)
                self.save_entries()
                self.clear_entries()
                messagebox.showinfo("Success", f"Entry for {date} deleted.")
                return

        messagebox.showerror("Error", f"No entry found for {date}.")

    def view_entries(self):
        if self.entries:
            result = "\n".join([f"Date: {entry['date']}\n{entry['content']}\n" for entry in self.entries])
            self.output_text.config(text=f"All Entries:\n{result}")
        else:
            self.output_text.config(text="No entries available.")

    def search_entries(self):
        search_term = self.date_entry.get()
        if not search_term:
            messagebox.showerror("Error", "Please enter a search term (date or keyword).")
            return

        found_entries = [entry for entry in self.entries if search_term.lower() in entry['date'].lower() or search_term.lower() in entry['content'].lower()]
        if found_entries:
            result = "\n".join([f"Date: {entry['date']}\n{entry['content']}\n" for entry in found_entries])
            self.output_text.config(text=f"Search Results:\n{result}")
        else:
            self.output_text.config(text="No entries found.")

    def list_entries(self):
        if self.entries:
            result = "\n".join([f"Date: {entry['date']}, Content: {entry['content'][:30]}..." for entry in self.entries])
            self.output_text.config(text=f"Entries List:\n{result}")
        else:
            self.output_text.config(text="No entries available.")

    def save_entries(self):
        with open("journal_entries.json", "w") as file:
            json.dump(self.entries, file)

    def load_entries(self):
        try:
            with open("journal_entries.json", "r") as file:
                self.entries = json.load(file)
        except FileNotFoundError:
            self.entries = []

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)


# Initialize the Application
root = tk.Tk()
app = JournalApp(root)

# Start the GUI loop
root.mainloop()

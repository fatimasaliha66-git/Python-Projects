import tkinter as tk
from tkinter import ttk, messagebox
import csv

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book Application")

        self.contacts = []

        # GUI Components
        self.create_widgets()
        self.load_contacts()

    def create_widgets(self):
        # Name Input
        self.name_label = ttk.Label(self.root, text="Name:")
        self.name_label.pack(pady=5)
        self.name_entry = ttk.Entry(self.root, width=40)
        self.name_entry.pack(pady=5)

        # Phone Input
        self.phone_label = ttk.Label(self.root, text="Phone:")
        self.phone_label.pack(pady=5)
        self.phone_entry = ttk.Entry(self.root, width=40)
        self.phone_entry.pack(pady=5)

        # Email Input
        self.email_label = ttk.Label(self.root, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = ttk.Entry(self.root, width=40)
        self.email_entry.pack(pady=5)

        # Buttons
        self.add_button = ttk.Button(self.root, text="Add Contact", command=self.add_contact)
        self.add_button.pack(pady=5)

        self.remove_button = ttk.Button(self.root, text="Remove Contact", command=self.remove_contact)
        self.remove_button.pack(pady=5)

        self.search_button = ttk.Button(self.root, text="Search Contact", command=self.search_contact)
        self.search_button.pack(pady=5)

        self.list_button = ttk.Button(self.root, text="List Contacts", command=self.list_contacts)
        self.list_button.pack(pady=5)

        self.export_button = ttk.Button(self.root, text="Export Contacts", command=self.export_contacts)
        self.export_button.pack(pady=5)

        self.import_button = ttk.Button(self.root, text="Import Contacts", command=self.import_contacts)
        self.import_button.pack(pady=5)

        # Output area
        self.output_text = ttk.Label(self.root, text="", justify="left")
        self.output_text.pack(pady=5)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if not name or not phone or not email:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        contact = {'name': name, 'phone': phone, 'email': email}
        self.contacts.append(contact)
        self.save_contacts()
        self.clear_entries()
        messagebox.showinfo("Success", "Contact added successfully!")

    def remove_contact(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter a name to remove.")
            return

        for contact in self.contacts:
            if contact['name'].lower() == name.lower():
                self.contacts.remove(contact)
                self.save_contacts()
                self.clear_entries()
                messagebox.showinfo("Success", f"Contact '{name}' removed.")
                return

        messagebox.showerror("Error", "Contact not found.")

    def search_contact(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter a name to search.")
            return

        found_contacts = [contact for contact in self.contacts if name.lower() in contact['name'].lower()]
        if found_contacts:
            result = "\n".join([f"Name: {contact['name']}, Phone: {contact['phone']}, Email: {contact['email']}" for contact in found_contacts])
            self.output_text.config(text=f"Search Results:\n{result}")
        else:
            self.output_text.config(text="No contacts found.")

    def list_contacts(self):
        if self.contacts:
            result = "\n".join([f"Name: {contact['name']}, Phone: {contact['phone']}, Email: {contact['email']}" for contact in self.contacts])
            self.output_text.config(text=f"Contacts:\n{result}")
        else:
            self.output_text.config(text="No contacts available.")

    def save_contacts(self):
        with open("contacts.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "phone", "email"])
            writer.writeheader()
            writer.writerows(self.contacts)

    def load_contacts(self):
        try:
            with open("contacts.csv", "r") as file:
                reader = csv.DictReader(file)
                self.contacts = [row for row in reader]
        except FileNotFoundError:
            self.contacts = []

    def import_contacts(self):
        try:
            with open("contacts.csv", "r") as file:
                reader = csv.DictReader(file)
                self.contacts = [row for row in reader]
            messagebox.showinfo("Success", "Contacts imported successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No contacts file found to import.")

    def export_contacts(self):
        if not self.contacts:
            messagebox.showerror("Error", "No contacts to export.")
            return
        self.save_contacts()
        messagebox.showinfo("Success", "Contacts exported successfully!")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)


# Initialize the Application
root = tk.Tk()
app = ContactBookApp(root)

# Start the GUI loop
root.mainloop()

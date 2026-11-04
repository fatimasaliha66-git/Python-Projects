import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip
import re


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator Tool")
        self.root.geometry("400x500")
        
        # Store password history
        self.password_history = []

        # Input fields and labels
        tk.Label(root, text="Password Length:").pack(pady=5)
        self.length_entry = tk.Entry(root)
        self.length_entry.pack(pady=5)

        self.use_special_chars = tk.BooleanVar()
        self.use_numbers = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)

        tk.Checkbutton(root, text="Include Special Characters", variable=self.use_special_chars).pack()
        tk.Checkbutton(root, text="Include Numbers", variable=self.use_numbers).pack()
        tk.Checkbutton(root, text="Include Uppercase Letters", variable=self.use_uppercase).pack()

        # Buttons
        tk.Button(root, text="Generate Password", command=self.generate_password).pack(pady=10)
        tk.Button(root, text="Validate Password", command=self.validate_password).pack(pady=10)
        tk.Button(root, text="Copy Password", command=self.copy_to_clipboard).pack(pady=10)
        tk.Button(root, text="Export Password History", command=self.export_password_history).pack(pady=10)

        # Output label
        self.output_label = tk.Label(root, text="Output will appear here", wraplength=300, justify="left")
        self.output_label.pack(pady=10)

        # Password strength indicator
        self.strength_label = tk.Label(root, text="Password Strength: Not Checked", fg="gray")
        self.strength_label.pack(pady=5)

        # Auto-generate password on startup
        self.auto_generate_password()

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            if length < 1:
                raise ValueError("Length must be at least 1.")
            
            char_set = string.ascii_lowercase
            if self.use_uppercase.get():
                char_set += string.ascii_uppercase
            if self.use_numbers.get():
                char_set += string.digits
            if self.use_special_chars.get():
                char_set += string.punctuation

            password = ''.join(random.choice(char_set) for _ in range(length))
            self.password_history.append(password)
            self.output_label.config(text=f"Generated Password: {password}")
            self.update_password_strength(password)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def validate_password(self):
        password = self.output_label.cget("text").replace("Generated Password: ", "")
        if not password:
            messagebox.showerror("Error", "No password generated to validate.")
            return
        
        errors = []
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter.")
        if self.use_uppercase.get() and not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter.")
        if self.use_numbers.get() and not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one number.")
        if self.use_special_chars.get() and not any(c in string.punctuation for c in password):
            errors.append("Password must contain at least one special character.")
        
        if errors:
            self.output_label.config(text="Validation Errors:\n" + "\n".join(errors))
        else:
            self.output_label.config(text="Password is valid!")

    def copy_to_clipboard(self):
        password = self.output_label.cget("text").replace("Generated Password: ", "")
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard.")
        else:
            messagebox.showerror("Error", "No password generated to copy.")

    def export_password_history(self):
        if not self.password_history:
            messagebox.showerror("Error", "No password history to export.")
            return

        with open("password_history.txt", "w") as f:
            for password in self.password_history:
                f.write(password + "\n")
        messagebox.showinfo("Success", "Password history exported to password_history.txt.")

    def auto_generate_password(self):
        """Auto-generate a password when the app starts."""
        length = 12  # Default length
        char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        password = ''.join(random.choice(char_set) for _ in range(length))
        self.password_history.append(password)
        self.output_label.config(text=f"Generated Password: {password}")
        self.update_password_strength(password)

    def update_password_strength(self, password):
        """Update password strength indicator."""
        if len(password) < 8:
            strength = "Weak"
            color = "red"
        elif len(password) < 12:
            strength = "Moderate"
            color = "orange"
        else:
            strength = "Strong"
            color = "green"
        
        self.strength_label.config(text=f"Password Strength: {strength}", fg=color)


# Create the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import qrcode

class LibraryManagementSystem:
    def __init__(self, root):
        self.books = {}  # Dictionary to store books
        self.borrowed_books = {}  # Dictionary to track borrowed books
        self.book_counter = 1  # Unique book ID counter
        self.root = root
        self.root.title("Library Management System")
        self.load_books()

        # Create the GUI components
        self.create_widgets()

    def load_books(self):
        """Load books from a JSON file if it exists."""
        if os.path.exists('books.json'):
            with open('books.json', 'r') as f:
                data = json.load(f)
                self.books = data.get('books', {})
                self.book_counter = data.get('book_counter', 1)

    def save_books(self):
        """Save books to a JSON file."""
        data = {'books': self.books, 'book_counter': self.book_counter}
        with open('books.json', 'w') as f:
            json.dump(data, f)

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Library Management System", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Book Title Input
        book_title_label = tk.Label(self.root, text="Book Title:", font=("Arial", 12))
        book_title_label.pack()
        self.book_title_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.book_title_entry.pack()

        # Author Input
        book_author_label = tk.Label(self.root, text="Author:", font=("Arial", 12))
        book_author_label.pack()
        self.book_author_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.book_author_entry.pack()

        # Book ID Input
        book_id_label = tk.Label(self.root, text="Book ID (for actions):", font=("Arial", 12))
        book_id_label.pack()
        self.book_id_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.book_id_entry.pack()

        # User Input (For Borrowing)
        user_label = tk.Label(self.root, text="Borrower Name (for borrowing):", font=("Arial", 12))
        user_label.pack()
        self.user_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.user_entry.pack()

        # Discount Input
        discount_label = tk.Label(self.root, text="Discount (in %):", font=("Arial", 12))
        discount_label.pack()
        self.discount_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.discount_entry.pack()

        # Buttons for actions
        add_book_button = tk.Button(self.root, text="Add Book", command=self.add_book, width=20, font=("Arial", 12))
        add_book_button.pack(pady=5)

        remove_book_button = tk.Button(self.root, text="Remove Book", command=self.remove_book, width=20, font=("Arial", 12))
        remove_book_button.pack(pady=5)

        check_availability_button = tk.Button(self.root, text="Check Availability", command=self.check_availability, width=20, font=("Arial", 12))
        check_availability_button.pack(pady=5)

        borrow_book_button = tk.Button(self.root, text="Borrow Book", command=self.borrow_book, width=20, font=("Arial", 12))
        borrow_book_button.pack(pady=5)

        return_book_button = tk.Button(self.root, text="Return Book", command=self.return_book, width=20, font=("Arial", 12))
        return_book_button.pack(pady=5)

        # Search Button
        search_button = tk.Button(self.root, text="Search Book", command=self.search_book, width=20, font=("Arial", 12))
        search_button.pack(pady=5)

        # Output area
        output_label = tk.Label(self.root, text="Output:", font=("Arial", 12, "bold"))
        output_label.pack(pady=10)
        self.output_text = tk.Text(self.root, height=10, width=60, font=("Arial", 10))
        self.output_text.pack()

    def send_email(self, to_email, subject, body):
        """Send an email notification."""
        sender_email = "your_email@example.com"
        password = "your_email_password"
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.example.com', 587) as server:
                server.starttls()
                server.login(sender_email, password)
                text = msg.as_string()
                server.sendmail(sender_email, to_email, text)
            messagebox.showinfo("Success", "Email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {e}")

    def generate_qr_code(self, book_id):
        """Generate a QR code for the book ID."""
        qr = qrcode.make(book_id)
        qr.save(f"book_{book_id}.png")
        self.output_text.insert(tk.END, f"QR code generated for Book ID {book_id}.\n")

    def add_book(self):
        title = self.book_title_entry.get().strip()
        author = self.book_author_entry.get().strip()
        discount = self.discount_entry.get().strip()

        if not title or not author:
            messagebox.showerror("Input Error", "Please provide both title and author!")
            return

        try:
            discount = float(discount) if discount else 0.0  # Default to 0% if no discount is entered
        except ValueError:
            messagebox.showerror("Input Error", "Please provide a valid discount percentage!")
            return

        book_id = self.book_counter
        self.books[book_id] = {"title": title, "author": author, "is_borrowed": False, "discount": discount}
        self.book_counter += 1
        self.generate_qr_code(book_id)
        self.output_text.insert(tk.END, f"Book added: {title} by {author}. Book ID: {book_id}, Discount: {discount}%\n")
        self.save_books()
        self.clear_inputs()

    def remove_book(self):
        book_id = self.book_id_entry.get().strip()

        if not book_id.isdigit():
            messagebox.showerror("Input Error", "Please provide a valid Book ID!")
            return

        book_id = int(book_id)
        if book_id in self.books:
            removed_book = self.books.pop(book_id)
            self.output_text.insert(tk.END, f"Book removed: {removed_book['title']} by {removed_book['author']}\n")
            self.save_books()
        else:
            self.output_text.insert(tk.END, f"Book with ID {book_id} not found.\n")
        self.clear_inputs()

    def check_availability(self):
        book_id = self.book_id_entry.get().strip()

        if not book_id.isdigit():
            messagebox.showerror("Input Error", "Please provide a valid Book ID!")
            return

        book_id = int(book_id)
        if book_id in self.books:
            book = self.books[book_id]
            if book["is_borrowed"]:
                self.output_text.insert(tk.END, f"Book '{book['title']}' by {book['author']} is currently borrowed.\n")
            else:
                self.output_text.insert(tk.END, f"Book '{book['title']}' by {book['author']}' is available.\n")
        else:
            self.output_text.insert(tk.END, f"Book with ID {book_id} not found.\n")
        self.clear_inputs()

    def borrow_book(self):
        book_id = self.book_id_entry.get().strip()
        user = self.user_entry.get().strip()

        if not book_id.isdigit() or not user:
            messagebox.showerror("Input Error", "Please provide a valid Book ID and Borrower Name!")
            return

        book_id = int(book_id)
        if book_id in self.books:
            book = self.books[book_id]
            if book["is_borrowed"]:
                self.output_text.insert(tk.END, f"Sorry, the book '{book['title']}' is already borrowed.\n")
            else:
                book["is_borrowed"] = True
                self.borrowed_books[book_id] = user
                self.apply_discount(book, user)  # Apply discount when borrowing
                self.send_email(user + "@example.com", "Book Borrowed", f"You have borrowed '{book['title']}' by {book['author']}.")
                self.output_text.insert(tk.END, f"{user} borrowed '{book['title']}' by {book['author']}.\n")
                self.save_books()
        else:
            self.output_text.insert(tk.END, f"Book with ID {book_id} not found.\n")
        self.clear_inputs()

    def return_book(self):
        book_id = self.book_id_entry.get().strip()

        if not book_id.isdigit():
            messagebox.showerror("Input Error", "Please provide a valid Book ID!")
            return

        book_id = int(book_id)
        if book_id in self.books and book_id in self.borrowed_books:
            book = self.books[book_id]
            user = self.borrowed_books.pop(book_id)
            book["is_borrowed"] = False
            self.send_email(user + "@example.com", "Book Returned", f"You have returned '{book['title']}' by {book['author']}.")
            self.output_text.insert(tk.END, f"Book '{book['title']}' by {book['author']} has been returned by {user}.\n")
            self.save_books()
        else:
            self.output_text.insert(tk.END, f"Book with ID {book_id} was not borrowed or not found.\n")
        self.clear_inputs()

    def search_book(self):
        title = self.book_title_entry.get().strip()
        author = self.book_author_entry.get().strip()

        results = []
        for book_id, book in self.books.items():
            if (title.lower() in book["title"].lower()) and (author.lower() in book["author"].lower()):
                results.append(f"ID: {book_id}, Title: {book['title']}, Author: {book['author']}, Discount: {book['discount']}%")
        
        if results:
            self.output_text.insert(tk.END, "\n".join(results) + "\n")
        else:
            self.output_text.insert(tk.END, "No books found matching the search criteria.\n")
        self.clear_inputs()

    def apply_discount(self, book, user):
        discount = book["discount"]
        # Assuming a fixed borrowing fee of 10 for simplicity
        borrowing_fee = 10
        discounted_fee = borrowing_fee - (borrowing_fee * (discount / 100))
        self.output_text.insert(tk.END, f"Discount applied for {user}. Final borrowing fee: ${discounted_fee}\n")

    def clear_inputs(self):
        """Clear all input fields."""
        self.book_title_entry.delete(0, tk.END)
        self.book_author_entry.delete(0, tk.END)
        self.book_id_entry.delete(0, tk.END)
        self.user_entry.delete(0, tk.END)
        self.discount_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()

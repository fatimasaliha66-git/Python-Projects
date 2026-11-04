import tkinter as tk
from tkinter import ttk, messagebox

# Caesar Cipher Encryption and Decryption
def caesar_encrypt(text, key):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shift = key % 26
            base = ord('A') if char.isupper() else ord('a')
            encrypted_text += chr((ord(char) - base + shift) % 26 + base)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, key):
    return caesar_encrypt(text, -key)

# Vigenère Cipher Encryption and Decryption
def vigenere_encrypt(text, key):
    encrypted_text = ""
    key = key.upper()
    key_index = 0

    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')
            encrypted_text += chr((ord(char) - base + shift) % 26 + base)
            key_index += 1
        else:
            encrypted_text += char
    return encrypted_text

def vigenere_decrypt(text, key):
    decrypted_text = ""
    key = key.upper()
    key_index = 0

    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')
            decrypted_text += chr((ord(char) - base - shift) % 26 + base)
            key_index += 1
        else:
            decrypted_text += char
    return decrypted_text

# GUI Application
class EncryptionToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Encryption and Decryption Tool")

        # Text Input Section
        self.text_label = ttk.Label(root, text="Enter Text:")
        self.text_label.pack(pady=5)
        self.text_entry = ttk.Entry(root, width=50)
        self.text_entry.pack(pady=5)

        # Key Section
        self.key_label = ttk.Label(root, text="Enter Key:")
        self.key_label.pack(pady=5)
        self.key_entry = ttk.Entry(root, width=50)
        self.key_entry.pack(pady=5)

        # Encryption Method Section
        self.cipher_label = ttk.Label(root, text="Select Cipher Method:")
        self.cipher_label.pack(pady=5)
        self.cipher_combobox = ttk.Combobox(root, values=["Caesar Cipher", "Vigenère Cipher"])
        self.cipher_combobox.pack(pady=5)
        self.cipher_combobox.current(0)  # Default to Caesar Cipher

        # Buttons for Encryption and Decryption
        self.encrypt_button = ttk.Button(root, text="Encrypt", command=self.encrypt_text)
        self.encrypt_button.pack(pady=5)
        self.decrypt_button = ttk.Button(root, text="Decrypt", command=self.decrypt_text)
        self.decrypt_button.pack(pady=5)

        # Output Section
        self.output_label = ttk.Label(root, text="Output:")
        self.output_label.pack(pady=5)
        self.output_text = ttk.Label(root, text="", wraplength=500, justify="left")
        self.output_text.pack(pady=5)

    def encrypt_text(self):
        text = self.text_entry.get()
        key = self.key_entry.get()

        if not text or not key:
            messagebox.showerror("Error", "Please enter both text and key.")
            return

        method = self.cipher_combobox.get()
        if method == "Caesar Cipher":
            try:
                key = int(key)
                encrypted = caesar_encrypt(text, key)
                self.output_text.config(text=f"Encrypted Text: {encrypted}")
            except ValueError:
                messagebox.showerror("Error", "Key for Caesar Cipher must be an integer.")
        elif method == "Vigenère Cipher":
            if not key.isalpha():
                messagebox.showerror("Error", "Key for Vigenère Cipher must contain only alphabetic characters.")
                return
            encrypted = vigenere_encrypt(text, key)
            self.output_text.config(text=f"Encrypted Text: {encrypted}")
        else:
            messagebox.showerror("Error", "Please select a cipher method.")

    def decrypt_text(self):
        text = self.text_entry.get()
        key = self.key_entry.get()

        if not text or not key:
            messagebox.showerror("Error", "Please enter both text and key.")
            return

        method = self.cipher_combobox.get()
        if method == "Caesar Cipher":
            try:
                key = int(key)
                decrypted = caesar_decrypt(text, key)
                self.output_text.config(text=f"Decrypted Text: {decrypted}")
            except ValueError:
                messagebox.showerror("Error", "Key for Caesar Cipher must be an integer.")
        elif method == "Vigenère Cipher":
            if not key.isalpha():
                messagebox.showerror("Error", "Key for Vigenère Cipher must contain only alphabetic characters.")
                return
            decrypted = vigenere_decrypt(text, key)
            self.output_text.config(text=f"Decrypted Text: {decrypted}")
        else:
            messagebox.showerror("Error", "Please select a cipher method.")

# Initialize Application
root = tk.Tk()
app = EncryptionToolApp(root)

# Start the application
root.mainloop()

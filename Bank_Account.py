import tkinter as tk
from tkinter import messagebox
import csv
import os
import hashlib

class BankAccount:
    def __init__(self, root):
        self.accounts = {}  # Dictionary to store account details
        self.root = root
        self.root.title("Bank Account System")
        self.api_key = "YOUR_API_KEY"  # For email/SMS functionality, add your API key here if needed
        self.load_accounts()
        self.create_widgets()

    def load_accounts(self):
        """Load accounts from a CSV file if it exists."""
        if os.path.exists('accounts.csv'):
            with open('accounts.csv', 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Create a dictionary of accounts where account name is the key
                    self.accounts[row['account_name']] = {
                        "balance": int(row['balance']),
                        "password": row['password'],
                        "transaction_history": row['transaction_history'].split('|')
                    }

    def save_accounts(self):
        """Save accounts to a CSV file."""
        with open('accounts.csv', 'w', newline='') as f:
            fieldnames = ['account_name', 'balance', 'password', 'transaction_history']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for account_name, details in self.accounts.items():
                transaction_history = '|'.join(details['transaction_history'])
                writer.writerow({
                    'account_name': account_name,
                    'balance': details['balance'],
                    'password': details['password'],
                    'transaction_history': transaction_history
                })

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Bank Account System", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Account Name Input
        account_label = tk.Label(self.root, text="Account Name:", font=("Arial", 12))
        account_label.pack()
        self.account_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.account_entry.pack()

        # Amount Input
        amount_label = tk.Label(self.root, text="Amount (for deposit/withdraw):", font=("Arial", 12))
        amount_label.pack()
        self.amount_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.amount_entry.pack()

        # Password Input
        password_label = tk.Label(self.root, text="Password:", font=("Arial", 12))
        password_label.pack()
        self.password_entry = tk.Entry(self.root, width=30, font=("Arial", 12), show="*")
        self.password_entry.pack()

        # Buttons for actions
        create_button = tk.Button(self.root, text="Create Account", command=self.create_account, width=20, font=("Arial", 12))
        create_button.pack(pady=5)

        deposit_button = tk.Button(self.root, text="Deposit", command=self.deposit, width=20, font=("Arial", 12))
        deposit_button.pack(pady=5)

        withdraw_button = tk.Button(self.root, text="Withdraw", command=self.withdraw, width=20, font=("Arial", 12))
        withdraw_button.pack(pady=5)

        balance_button = tk.Button(self.root, text="Check Balance", command=self.check_balance, width=20, font=("Arial", 12))
        balance_button.pack(pady=5)

        history_button = tk.Button(self.root, text="Transaction History", command=self.transaction_history, width=20, font=("Arial", 12))
        history_button.pack(pady=5)

        # Output area
        output_label = tk.Label(self.root, text="Output:", font=("Arial", 12, "bold"))
        output_label.pack(pady=10)
        self.output_text = tk.Text(self.root, height=10, width=50, font=("Arial", 10))
        self.output_text.pack()

    def hash_password(self, password):
        """Hashes the password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_account(self):
        account_name = self.account_entry.get().strip()
        initial_balance = self.amount_entry.get().strip()
        password = self.password_entry.get().strip()

        if not account_name or not initial_balance.isdigit() or not password:
            messagebox.showerror("Input Error", "Please provide a valid account name, initial balance, and password!")
            return

        initial_balance = int(initial_balance)
        hashed_password = self.hash_password(password)

        if account_name in self.accounts:
            self.output_text.insert(tk.END, f"Account '{account_name}' already exists.\n")
        else:
            self.accounts[account_name] = {
                "balance": initial_balance,
                "password": hashed_password,
                "transaction_history": [f"Account created with initial balance: {initial_balance}"]
            }
            self.output_text.insert(tk.END, f"Account '{account_name}' created with initial balance of {initial_balance}.\n")
            self.save_accounts()
        self.clear_inputs()

    def verify_account(self, account_name, password):
        """Verifies the account password."""
        if account_name in self.accounts and self.accounts[account_name]["password"] == self.hash_password(password):
            return True
        return False

    def deposit(self):
        account_name = self.account_entry.get().strip()
        amount = self.amount_entry.get().strip()
        password = self.password_entry.get().strip()

        if not account_name or not amount.isdigit() or not password:
            messagebox.showerror("Input Error", "Please provide a valid account name, deposit amount, and password!")
            return

        amount = int(amount)
        if self.verify_account(account_name, password):
            if account_name in self.accounts:
                if amount > 0:
                    self.accounts[account_name]["balance"] += amount
                    self.accounts[account_name]["transaction_history"].append(f"Deposited {amount}")
                    self.output_text.insert(tk.END, f"Deposited {amount} into account '{account_name}'. New balance: {self.accounts[account_name]['balance']}.\n")
                    self.save_accounts()
                else:
                    self.output_text.insert(tk.END, "Deposit amount must be positive.\n")
            else:
                self.output_text.insert(tk.END, f"Account '{account_name}' does not exist.\n")
        else:
            self.output_text.insert(tk.END, "Invalid account name or password.\n")
        self.clear_inputs()

    def withdraw(self):
        account_name = self.account_entry.get().strip()
        amount = self.amount_entry.get().strip()
        password = self.password_entry.get().strip()

        if not account_name or not amount.isdigit() or not password:
            messagebox.showerror("Input Error", "Please provide a valid account name, withdrawal amount, and password!")
            return

        amount = int(amount)
        if self.verify_account(account_name, password):
            if account_name in self.accounts:
                if amount <= 0:
                    self.output_text.insert(tk.END, "Withdrawal amount must be positive.\n")
                elif self.accounts[account_name]["balance"] >= amount:
                    self.accounts[account_name]["balance"] -= amount
                    self.accounts[account_name]["transaction_history"].append(f"Withdrew {amount}")
                    self.output_text.insert(tk.END, f"Withdrew {amount} from account '{account_name}'. New balance: {self.accounts[account_name]['balance']}.\n")
                    self.save_accounts()
                else:
                    self.output_text.insert(tk.END, f"Insufficient funds in account '{account_name}' for withdrawal of {amount}.\n")
            else:
                self.output_text.insert(tk.END, f"Account '{account_name}' does not exist.\n")
        else:
            self.output_text.insert(tk.END, "Invalid account name or password.\n")
        self.clear_inputs()

    def check_balance(self):
        account_name = self.account_entry.get().strip()
        password = self.password_entry.get().strip()

        if not account_name or not password:
            messagebox.showerror("Input Error", "Please provide a valid account name and password!")
            return

        if self.verify_account(account_name, password):
            if account_name in self.accounts:
                self.output_text.insert(tk.END, f"Account '{account_name}' balance: {self.accounts[account_name]['balance']}.\n")
            else:
                self.output_text.insert(tk.END, f"Account '{account_name}' does not exist.\n")
        else:
            self.output_text.insert(tk.END, "Invalid account name or password.\n")
        self.clear_inputs()

    def transaction_history(self):
        account_name = self.account_entry.get().strip()
        password = self.password_entry.get().strip()

        if not account_name or not password:
            messagebox.showerror("Input Error", "Please provide a valid account name and password!")
            return

        if self.verify_account(account_name, password):
            if account_name in self.accounts:
                self.output_text.insert(tk.END, f"Transaction history for account '{account_name}':\n")
                for transaction in self.accounts[account_name]["transaction_history"]:
                    self.output_text.insert(tk.END, f"  - {transaction}\n")
            else:
                self.output_text.insert(tk.END, f"Account '{account_name}' does not exist.\n")
        else:
            self.output_text.insert(tk.END, "Invalid account name or password.\n")
        self.clear_inputs()

    def clear_inputs(self):
        """Clear the input fields."""
        self.account_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = BankAccount(root)
    root.mainloop()

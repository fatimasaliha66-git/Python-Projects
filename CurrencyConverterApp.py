import tkinter as tk
from tkinter import ttk, messagebox

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        # Dictionary to store currency rates (initial rates are just examples)
        self.currencies = {
            "USD": 1.0,   # base currency (USD)
            "EUR": 0.85,
            "GBP": 0.75,
            "INR": 74.5,
            "AUD": 1.3
        }

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title_label = ttk.Label(self.root, text="Currency Converter", font=("Arial", 20))
        self.title_label.pack(pady=10)

        # Amount Entry
        self.amount_label = ttk.Label(self.root, text="Amount to Convert:")
        self.amount_label.pack(pady=5)
        self.amount_entry = ttk.Entry(self.root, width=20)
        self.amount_entry.pack(pady=5)

        # From Currency Selection
        self.from_currency_label = ttk.Label(self.root, text="From Currency:")
        self.from_currency_label.pack(pady=5)
        self.from_currency_combobox = ttk.Combobox(self.root, values=list(self.currencies.keys()), state="readonly")
        self.from_currency_combobox.pack(pady=5)

        # To Currency Selection
        self.to_currency_label = ttk.Label(self.root, text="To Currency:")
        self.to_currency_label.pack(pady=5)
        self.to_currency_combobox = ttk.Combobox(self.root, values=list(self.currencies.keys()), state="readonly")
        self.to_currency_combobox.pack(pady=5)

        # Convert Button
        self.convert_button = ttk.Button(self.root, text="Convert", command=self.convert)
        self.convert_button.pack(pady=10)

        # Result Display
        self.result_label = ttk.Label(self.root, text="Converted Value: ", font=("Arial", 14))
        self.result_label.pack(pady=10)

        # Update Currency Button
        self.update_button = ttk.Button(self.root, text="Update Currency Rate", command=self.update_exchange_rate)
        self.update_button.pack(pady=5)

        # Add Currency Button
        self.add_currency_button = ttk.Button(self.root, text="Add Currency", command=self.add_currency)
        self.add_currency_button.pack(pady=5)

    def convert(self):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")
            return

        from_currency = self.from_currency_combobox.get()
        to_currency = self.to_currency_combobox.get()

        if not from_currency or not to_currency:
            messagebox.showerror("Missing Currency", "Please select both From and To currencies.")
            return

        if from_currency == to_currency:
            messagebox.showinfo("No Conversion", "The currencies are the same. No conversion needed.")
            return

        # Conversion formula
        converted_amount = amount * self.currencies[to_currency] / self.currencies[from_currency]
        self.result_label.config(text=f"Converted Value: {converted_amount:.2f} {to_currency}")

    def update_exchange_rate(self):
        def apply_update():
            currency = currency_combobox.get()
            new_rate = rate_entry.get()

            try:
                new_rate = float(new_rate)
                if currency in self.currencies:
                    self.currencies[currency] = new_rate
                    messagebox.showinfo("Success", f"Exchange rate for {currency} updated to {new_rate}.")
                else:
                    messagebox.showerror("Error", f"Currency {currency} not found.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid exchange rate.")

        # New window to update the exchange rate
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Exchange Rate")

        currency_label = ttk.Label(update_window, text="Select Currency:")
        currency_label.pack(pady=5)

        currency_combobox = ttk.Combobox(update_window, values=list(self.currencies.keys()), state="readonly")
        currency_combobox.pack(pady=5)

        rate_label = ttk.Label(update_window, text="New Exchange Rate:")
        rate_label.pack(pady=5)

        rate_entry = ttk.Entry(update_window)
        rate_entry.pack(pady=5)

        update_button = ttk.Button(update_window, text="Update", command=apply_update)
        update_button.pack(pady=5)

        close_button = ttk.Button(update_window, text="Close", command=update_window.destroy)
        close_button.pack(pady=5)

    def add_currency(self):
        def apply_add():
            new_currency = currency_entry.get()
            new_rate = rate_entry.get()

            try:
                new_rate = float(new_rate)
                if new_currency not in self.currencies:
                    self.currencies[new_currency] = new_rate
                    self.from_currency_combobox['values'] = list(self.currencies.keys())
                    self.to_currency_combobox['values'] = list(self.currencies.keys())
                    messagebox.showinfo("Success", f"Currency {new_currency} added with rate {new_rate}.")
                else:
                    messagebox.showerror("Error", f"Currency {new_currency} already exists.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid exchange rate.")

        # New window to add a new currency
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Currency")

        currency_label = ttk.Label(add_window, text="Currency Code (e.g., JPY):")
        currency_label.pack(pady=5)

        currency_entry = ttk.Entry(add_window)
        currency_entry.pack(pady=5)

        rate_label = ttk.Label(add_window, text="Exchange Rate:")
        rate_label.pack(pady=5)

        rate_entry = ttk.Entry(add_window)
        rate_entry.pack(pady=5)

        add_button = ttk.Button(add_window, text="Add Currency", command=apply_add)
        add_button.pack(pady=5)

        close_button = ttk.Button(add_window, text="Close", command=add_window.destroy)
        close_button.pack(pady=5)

# Initialize the Application
root = tk.Tk()
app = CurrencyConverterApp(root)

# Start the GUI loop
root.mainloop()

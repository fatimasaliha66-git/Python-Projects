import tkinter as tk
from tkinter import ttk, messagebox

# Cart Class to handle cart functionality
class Cart:
    def __init__(self):
        self.items = {}  # {item_name: (price, quantity)}

    def add_to_cart(self, item, price, quantity):
        if item in self.items:
            # Update the price (if price is different) and increase quantity
            self.items[item] = (price, self.items[item][1] + quantity)
        else:
            self.items[item] = (price, quantity)  # Add new item with specified price and quantity

    def remove_from_cart(self, item):
        if item in self.items:
            del self.items[item]
        else:
            messagebox.showerror("Error", "Item not in cart.")

    def calculate_total(self):
        total = sum(price * quantity for price, quantity in self.items.values())
        return total

    def apply_discount(self, discount):
        total = self.calculate_total()
        discount_amount = total * (discount / 100)
        return total - discount_amount

    def view_cart(self):
        return self.items

    def view_prices(self):
        return {item: price for item, (price, _) in self.items.items()}


# GUI Application
class CartApp:
    def __init__(self, root):
        self.cart = Cart()

        # Setup Window
        self.root = root
        self.root.title("Simple E-commerce Cart System")

        # Create Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)

        # Tab 1: Add Items
        self.add_items_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_items_tab, text="Add Items")

        # Tab 2: View Cart
        self.view_cart_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_cart_tab, text="View Cart")

        # Tab 3: View Prices
        self.view_prices_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_prices_tab, text="View Prices")

        # Add Items Tab Content
        self.item_label = ttk.Label(self.add_items_tab, text="Item Name:")
        self.item_label.pack(pady=5)
        self.item_entry = ttk.Entry(self.add_items_tab, width=30)
        self.item_entry.pack(pady=5)

        self.quantity_label = ttk.Label(self.add_items_tab, text="Quantity:")
        self.quantity_label.pack(pady=5)
        self.quantity_entry = ttk.Entry(self.add_items_tab, width=30)
        self.quantity_entry.pack(pady=5)

        self.price_label = ttk.Label(self.add_items_tab, text="Price per Item ($):")
        self.price_label.pack(pady=5)
        self.price_entry = ttk.Entry(self.add_items_tab, width=30)
        self.price_entry.pack(pady=5)

        self.add_button = ttk.Button(self.add_items_tab, text="Add to Cart", command=self.add_to_cart)
        self.add_button.pack(pady=5)

        self.discount_label = ttk.Label(self.add_items_tab, text="Discount (%)")
        self.discount_label.pack(pady=5)
        self.discount_entry = ttk.Entry(self.add_items_tab, width=10)
        self.discount_entry.pack(pady=5)

        self.apply_discount_button = ttk.Button(self.add_items_tab, text="Apply Discount", command=self.apply_discount)
        self.apply_discount_button.pack(pady=5)

        self.total_label = ttk.Label(self.add_items_tab, text="Total: $0.00")
        self.total_label.pack(pady=10)

        # View Cart Tab Content
        self.cart_button = ttk.Button(self.view_cart_tab, text="View Cart", command=self.view_cart)
        self.cart_button.pack(pady=5)

        # View Prices Tab Content
        self.view_prices_button = ttk.Button(self.view_prices_tab, text="View Prices", command=self.view_prices)
        self.view_prices_button.pack(pady=5)

    def add_to_cart(self):
        item = self.item_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        # Input validation
        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid quantity and price.")
            return

        if item and quantity > 0 and price > 0:
            self.cart.add_to_cart(item, price, quantity)
            messagebox.showinfo("Success", f"{item} (x{quantity}) added to cart!")
            self.item_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please provide valid item name, quantity, and price.")

    def view_cart(self):
        cart_items = self.cart.view_cart()
        if cart_items:
            cart_window = tk.Toplevel(self.root)
            cart_window.title("Your Cart")
            cart_frame = ttk.Frame(cart_window, padding="10")
            cart_frame.pack()

            for item, (price, quantity) in cart_items.items():
                ttk.Label(cart_frame, text=f"{item} - ${price} x {quantity}").pack(anchor=tk.W)

            total = self.cart.calculate_total()
            ttk.Label(cart_frame, text=f"Total: ${total:.2f}").pack(pady=5)

            remove_button = ttk.Button(cart_frame, text="Remove Item", command=lambda: self.remove_item(cart_window))
            remove_button.pack(pady=5)
        else:
            messagebox.showinfo("Cart Empty", "Your cart is empty.")

    def remove_item(self, cart_window):
        item = self.item_entry.get()
        if item:
            self.cart.remove_from_cart(item)
            messagebox.showinfo("Removed", f"{item} removed from cart!")
            cart_window.destroy()
        else:
            messagebox.showerror("Error", "Please specify the item to remove.")

    def apply_discount(self):
        try:
            discount = float(self.discount_entry.get())
            if 0 <= discount <= 100:
                total_after_discount = self.cart.apply_discount(discount)
                self.total_label.config(text=f"Total after discount: ${total_after_discount:.2f}")
            else:
                messagebox.showerror("Error", "Discount must be between 0 and 100.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid discount.")

    def view_prices(self):
        prices = self.cart.view_prices()
        if prices:
            prices_window = tk.Toplevel(self.root)
            prices_window.title("Item Prices")
            prices_frame = ttk.Frame(prices_window, padding="10")
            prices_frame.pack()

            for item, price in prices.items():
                ttk.Label(prices_frame, text=f"{item} - ${price}").pack(anchor=tk.W)
        else:
            messagebox.showinfo("No Items", "Your cart is empty.")


# Initialize Application
root = tk.Tk()
app = CartApp(root)

# Start the application
root.mainloop()

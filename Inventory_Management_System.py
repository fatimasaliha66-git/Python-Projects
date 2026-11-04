import tkinter as tk
from tkinter import simpledialog


class InventoryManagementSystem:
    def __init__(self):
        self.inventory = {}  # Store inventory items
        self.item_counter = 1  # Unique item ID counter
        self.total_profit = 0  # Tracker for total profit
        self.total_loss = 0  # Tracker for total loss

    def add_item(self, name, quantity, purchase_price, selling_price):
        item_id = self.item_counter
        self.inventory[item_id] = {
            "name": name,
            "quantity": quantity,
            "purchase_price": purchase_price,
            "selling_price": selling_price,
        }
        self.item_counter += 1
        return f"Item added: {name} (ID: {item_id})"

    def remove_item(self, item_id):
        if item_id in self.inventory:
            removed_item = self.inventory.pop(item_id)
            return f"Item removed: {removed_item['name']} (ID: {item_id})"
        return f"Item ID {item_id} not found."

    def update_stock(self, item_id, quantity):
        if item_id in self.inventory:
            self.inventory[item_id]["quantity"] = quantity
            return f"Stock updated for {self.inventory[item_id]['name']} (ID: {item_id})"
        return f"Item ID {item_id} not found."

    def add_quantity(self, item_id, quantity):
        if item_id in self.inventory:
            self.inventory[item_id]["quantity"] += quantity
            return f"Added {quantity} to {self.inventory[item_id]['name']} (ID: {item_id})"
        return f"Item ID {item_id} not found."

    def view_inventory(self):
        if not self.inventory:
            return "Inventory is empty."
        return "\n".join(
            f"ID {item_id}: {item['name']} - Qty: {item['quantity']}"
            for item_id, item in self.inventory.items()
        )

    def record_sale(self, item_id, quantity_sold):
        if item_id in self.inventory:
            item = self.inventory[item_id]
            if item["quantity"] >= quantity_sold:
                item["quantity"] -= quantity_sold
                profit = (item["selling_price"] - item["purchase_price"]) * quantity_sold
                if profit > 0:
                    self.total_profit += profit
                else:
                    self.total_loss += abs(profit)
                return f"Sale recorded for {item['name']} (ID: {item_id})"
            return f"Insufficient stock for {item['name']} (ID: {item_id})."
        return f"Item ID {item_id} not found."

    def purchase_item(self, item_id, quantity_purchased):
        if item_id in self.inventory:
            self.inventory[item_id]["quantity"] += quantity_purchased
            return f"Purchase recorded for {self.inventory[item_id]['name']} (ID: {item_id})"
        return f"Item ID {item_id} not found."

    def calculate_total_profit(self):
        return f"Total Profit: {self.total_profit}"

    def calculate_total_loss(self):
        return f"Total Loss: {self.total_loss}"


class InventoryGUI:
    def __init__(self, root):
        self.system = InventoryManagementSystem()

        self.root = root
        self.root.title("Inventory Management System")

        self.output_label = tk.Label(
            root, text="Output will appear here", fg="blue", wraplength=400, justify="left", font=("Helvetica", 14)
        )
        self.output_label.pack(pady=10)

        self.actions = [
            ("Add Item", self.add_item),
            ("Remove Item", self.remove_item),
            ("Update Stock", self.update_stock),
            ("Add Quantity", self.add_quantity),
            ("View Inventory", self.view_inventory),
            ("Record Sale", self.record_sale),
            ("Record Purchase", self.purchase_item),
            ("View Total Profit", self.view_profit),
            ("View Total Loss", self.view_loss),
            ("Exit", root.quit),
        ]

        self.action_frame = tk.Frame(root)
        self.action_frame.pack()

        for i, (label, command) in enumerate(self.actions):
            tk.Button(
                self.action_frame, text=label, command=command, font=("Helvetica", 12)
            ).grid(row=i // 3, column=i % 3, padx=5, pady=5)

    def add_item(self):
        name = self.simple_input("Enter item name:")
        if name:
            try:
                quantity = self.get_numeric_input("Enter quantity:")
                purchase_price = self.get_numeric_input("Enter purchase price:", float)
                selling_price = self.get_numeric_input("Enter selling price:", float)
                output = self.system.add_item(name, quantity, purchase_price, selling_price)
                self.update_output(output)
            except ValueError:
                self.update_output("Invalid input. Please enter valid numbers.")

    def remove_item(self):
        item_id = self.get_numeric_input("Enter item ID to remove:", int)
        output = self.system.remove_item(item_id)
        self.update_output(output)

    def update_stock(self):
        item_id = self.get_numeric_input("Enter item ID to update stock:", int)
        quantity = self.get_numeric_input("Enter new quantity:", int)
        output = self.system.update_stock(item_id, quantity)
        self.update_output(output)

    def add_quantity(self):
        item_id = self.get_numeric_input("Enter item ID to add quantity:", int)
        quantity = self.get_numeric_input("Enter quantity to add:", int)
        output = self.system.add_quantity(item_id, quantity)
        self.update_output(output)

    def view_inventory(self):
        self.update_output(self.system.view_inventory())

    def record_sale(self):
        item_id = self.get_numeric_input("Enter item ID for sale:", int)
        quantity_sold = self.get_numeric_input("Enter quantity sold:", int)
        output = self.system.record_sale(item_id, quantity_sold)
        self.update_output(output)

    def purchase_item(self):
        item_id = self.get_numeric_input("Enter item ID to purchase:", int)
        quantity_purchased = self.get_numeric_input("Enter quantity purchased:", int)
        output = self.system.purchase_item(item_id, quantity_purchased)
        self.update_output(output)

    def view_profit(self):
        self.update_output(self.system.calculate_total_profit())

    def view_loss(self):
        self.update_output(self.system.calculate_total_loss())

    def update_output(self, message):
        self.output_label.config(text=message)

    def simple_input(self, prompt):
        return simpledialog.askstring("Input", prompt)

    def get_numeric_input(self, prompt, cast_type=int):
        value = self.simple_input(prompt)
        if value:
            return cast_type(value)
        raise ValueError("Invalid numeric input")


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryGUI(root)
    root.mainloop()

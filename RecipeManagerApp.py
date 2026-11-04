import tkinter as tk
from tkinter import ttk, messagebox
import json

class RecipeManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Manager")

        self.recipes = []

        # GUI Components
        self.create_widgets()
        self.load_recipes()

    def create_widgets(self):
        # Name Input
        self.name_label = ttk.Label(self.root, text="Recipe Name:")
        self.name_label.pack(pady=5)
        self.name_entry = ttk.Entry(self.root, width=40)
        self.name_entry.pack(pady=5)

        # Ingredients Input
        self.ingredients_label = ttk.Label(self.root, text="Ingredients (comma separated):")
        self.ingredients_label.pack(pady=5)
        self.ingredients_entry = ttk.Entry(self.root, width=40)
        self.ingredients_entry.pack(pady=5)

        # Instructions Input
        self.instructions_label = ttk.Label(self.root, text="Instructions:")
        self.instructions_label.pack(pady=5)
        self.instructions_entry = ttk.Entry(self.root, width=40)
        self.instructions_entry.pack(pady=5)

        # Category Input
        self.category_label = ttk.Label(self.root, text="Category (e.g., Dessert, Main Course):")
        self.category_label.pack(pady=5)
        self.category_entry = ttk.Entry(self.root, width=40)
        self.category_entry.pack(pady=5)

        # Buttons
        self.add_button = ttk.Button(self.root, text="Add Recipe", command=self.add_recipe)
        self.add_button.pack(pady=5)

        self.remove_button = ttk.Button(self.root, text="Remove Recipe", command=self.remove_recipe)
        self.remove_button.pack(pady=5)

        self.search_button = ttk.Button(self.root, text="Search Recipe", command=self.search_recipe)
        self.search_button.pack(pady=5)

        self.view_button = ttk.Button(self.root, text="View Recipe", command=self.view_recipe)
        self.view_button.pack(pady=5)

        self.list_button = ttk.Button(self.root, text="List Recipes", command=self.list_recipes)
        self.list_button.pack(pady=5)

        self.export_button = ttk.Button(self.root, text="Export Recipes", command=self.export_recipes)
        self.export_button.pack(pady=5)

        self.import_button = ttk.Button(self.root, text="Import Recipes", command=self.import_recipes)
        self.import_button.pack(pady=5)

        # Output area
        self.output_text = ttk.Label(self.root, text="", justify="left")
        self.output_text.pack(pady=5)

    def add_recipe(self):
        name = self.name_entry.get()
        ingredients = self.ingredients_entry.get().split(',')
        instructions = self.instructions_entry.get()
        category = self.category_entry.get()

        if not name or not ingredients or not instructions or not category:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        recipe = {'name': name, 'ingredients': ingredients, 'instructions': instructions, 'category': category}
        self.recipes.append(recipe)
        self.save_recipes()
        self.clear_entries()
        messagebox.showinfo("Success", "Recipe added successfully!")

    def remove_recipe(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter a name to remove.")
            return

        for recipe in self.recipes:
            if recipe['name'].lower() == name.lower():
                self.recipes.remove(recipe)
                self.save_recipes()
                self.clear_entries()
                messagebox.showinfo("Success", f"Recipe '{name}' removed.")
                return

        messagebox.showerror("Error", "Recipe not found.")

    def search_recipe(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter a name to search.")
            return

        found_recipes = [recipe for recipe in self.recipes if name.lower() in recipe['name'].lower()]
        if found_recipes:
            result = "\n".join([f"Name: {recipe['name']}, Category: {recipe['category']}" for recipe in found_recipes])
            self.output_text.config(text=f"Search Results:\n{result}")
        else:
            self.output_text.config(text="No recipes found.")

    def view_recipe(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter a name to view.")
            return

        for recipe in self.recipes:
            if recipe['name'].lower() == name.lower():
                self.output_text.config(text=f"Recipe: {recipe['name']}\nCategory: {recipe['category']}\nIngredients: {', '.join(recipe['ingredients'])}\nInstructions: {recipe['instructions']}")
                return

        messagebox.showerror("Error", "Recipe not found.")

    def list_recipes(self):
        if self.recipes:
            result = "\n".join([f"Name: {recipe['name']}, Category: {recipe['category']}" for recipe in self.recipes])
            self.output_text.config(text=f"Recipes:\n{result}")
        else:
            self.output_text.config(text="No recipes available.")

    def save_recipes(self):
        with open("recipes.json", "w") as file:
            json.dump(self.recipes, file)

    def load_recipes(self):
        try:
            with open("recipes.json", "r") as file:
                self.recipes = json.load(file)
        except FileNotFoundError:
            self.recipes = []

    def import_recipes(self):
        try:
            with open("recipes.json", "r") as file:
                self.recipes = json.load(file)
            messagebox.showinfo("Success", "Recipes imported successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No recipes file found to import.")

    def export_recipes(self):
        if not self.recipes:
            messagebox.showerror("Error", "No recipes to export.")
            return
        self.save_recipes()
        messagebox.showinfo("Success", "Recipes exported successfully!")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.ingredients_entry.delete(0, tk.END)
        self.instructions_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)


# Initialize the Application
root = tk.Tk()
app = RecipeManagerApp(root)

# Start the GUI loop
root.mainloop()

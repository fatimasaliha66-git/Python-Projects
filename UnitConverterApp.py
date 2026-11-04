import tkinter as tk
from tkinter import ttk, messagebox

class UnitConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter")

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title_label = ttk.Label(self.root, text="Unit Converter", font=("Arial", 20))
        self.title_label.pack(pady=10)

        # Value Entry
        self.value_label = ttk.Label(self.root, text="Enter Value:")
        self.value_label.pack(pady=5)
        self.value_entry = ttk.Entry(self.root, width=20)
        self.value_entry.pack(pady=5)

        # Unit Type Selection
        self.unit_type_label = ttk.Label(self.root, text="Select Conversion Type:")
        self.unit_type_label.pack(pady=5)
        self.unit_type_combobox = ttk.Combobox(self.root, values=["Temperature", "Length", "Weight", "Time", "Currency"], state="readonly")
        self.unit_type_combobox.pack(pady=5)
        self.unit_type_combobox.bind("<<ComboboxSelected>>", self.update_units)

        # From and To Units
        self.from_unit_label = ttk.Label(self.root, text="From Unit:")
        self.from_unit_label.pack(pady=5)
        self.from_unit_combobox = ttk.Combobox(self.root, state="readonly")
        self.from_unit_combobox.pack(pady=5)

        self.to_unit_label = ttk.Label(self.root, text="To Unit:")
        self.to_unit_label.pack(pady=5)
        self.to_unit_combobox = ttk.Combobox(self.root, state="readonly")
        self.to_unit_combobox.pack(pady=5)

        # Convert Button
        self.convert_button = ttk.Button(self.root, text="Convert", command=self.convert)
        self.convert_button.pack(pady=10)

        # Result Display
        self.result_label = ttk.Label(self.root, text="Converted Value: ", font=("Arial", 14))
        self.result_label.pack(pady=10)

    def update_units(self, event):
        unit_type = self.unit_type_combobox.get()

        if unit_type == "Temperature":
            self.update_temperature_units()
        elif unit_type == "Length":
            self.update_length_units()
        elif unit_type == "Weight":
            self.update_weight_units()
        elif unit_type == "Time":
            self.update_time_units()
        elif unit_type == "Currency":
            self.update_currency_units()

    def update_temperature_units(self):
        self.from_unit_combobox.config(values=["Celsius", "Fahrenheit", "Kelvin"])
        self.to_unit_combobox.config(values=["Celsius", "Fahrenheit", "Kelvin"])

    def update_length_units(self):
        self.from_unit_combobox.config(values=["Meters", "Kilometers", "Miles", "Feet", "Inches"])
        self.to_unit_combobox.config(values=["Meters", "Kilometers", "Miles", "Feet", "Inches"])

    def update_weight_units(self):
        self.from_unit_combobox.config(values=["Kilograms", "Grams", "Pounds", "Ounces"])
        self.to_unit_combobox.config(values=["Kilograms", "Grams", "Pounds", "Ounces"])

    def update_time_units(self):
        self.from_unit_combobox.config(values=["Seconds", "Minutes", "Hours", "Days"])
        self.to_unit_combobox.config(values=["Seconds", "Minutes", "Hours", "Days"])

    def update_currency_units(self):
        self.from_unit_combobox.config(values=["USD", "EUR", "GBP"])
        self.to_unit_combobox.config(values=["USD", "EUR", "GBP"])

    def convert(self):
        try:
            value = float(self.value_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        from_unit = self.from_unit_combobox.get()
        to_unit = self.to_unit_combobox.get()

        if not from_unit or not to_unit:
            messagebox.showerror("Missing Units", "Please select both From and To units.")
            return

        unit_type = self.unit_type_combobox.get()

        if unit_type == "Temperature":
            result = self.convert_temperature(value, from_unit, to_unit)
        elif unit_type == "Length":
            result = self.convert_length(value, from_unit, to_unit)
        elif unit_type == "Weight":
            result = self.convert_weight(value, from_unit, to_unit)
        elif unit_type == "Time":
            result = self.convert_time(value, from_unit, to_unit)
        elif unit_type == "Currency":
            result = self.convert_currency(value, from_unit, to_unit)

        self.result_label.config(text=f"Converted Value: {result}")

    def convert_temperature(self, value, from_unit, to_unit):
        if from_unit == to_unit:
            return value
        elif from_unit == "Celsius":
            if to_unit == "Fahrenheit":
                return (value * 9/5) + 32
            elif to_unit == "Kelvin":
                return value + 273.15
        elif from_unit == "Fahrenheit":
            if to_unit == "Celsius":
                return (value - 32) * 5/9
            elif to_unit == "Kelvin":
                return (value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin":
            if to_unit == "Celsius":
                return value - 273.15
            elif to_unit == "Fahrenheit":
                return (value - 273.15) * 9/5 + 32

    def convert_length(self, value, from_unit, to_unit):
        length_units = {
            "Meters": 1,
            "Kilometers": 1000,
            "Miles": 1609.34,
            "Feet": 0.3048,
            "Inches": 0.0254
        }
        value_in_meters = value * length_units[from_unit]
        return value_in_meters / length_units[to_unit]

    def convert_weight(self, value, from_unit, to_unit):
        weight_units = {
            "Kilograms": 1,
            "Grams": 1000,
            "Pounds": 2.20462,
            "Ounces": 35.274
        }
        value_in_kg = value / weight_units[from_unit]
        return value_in_kg * weight_units[to_unit]

    def convert_time(self, value, from_unit, to_unit):
        time_units = {
            "Seconds": 1,
            "Minutes": 60,
            "Hours": 3600,
            "Days": 86400
        }
        value_in_seconds = value * time_units[from_unit]
        return value_in_seconds / time_units[to_unit]

    def convert_currency(self, value, from_unit, to_unit):
        # Dummy exchange rates (just for the sake of example)
        exchange_rates = {
            "USD": {"EUR": 0.85, "GBP": 0.75},
            "EUR": {"USD": 1.18, "GBP": 0.88},
            "GBP": {"USD": 1.33, "EUR": 1.14}
        }
        if from_unit == to_unit:
            return value
        return value * exchange_rates[from_unit].get(to_unit, 1)

# Initialize the Application
root = tk.Tk()
app = UnitConverterApp(root)

# Start the GUI loop
root.mainloop()

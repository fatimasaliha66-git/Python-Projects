import tkinter as tk
from tkinter import messagebox


class WeatherForecastingTool:
    def __init__(self, root):
        self.city_forecasts = {}  # Dictionary to store forecasts
        self.root = root
        self.root.title("Weather Forecasting Tool")

        # Create the GUI components
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Weather Forecasting Tool", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # City Input
        city_label = tk.Label(self.root, text="City:", font=("Arial", 12))
        city_label.pack()
        self.city_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.city_entry.pack()

        # Forecast Input
        forecast_label = tk.Label(self.root, text="Forecast:", font=("Arial", 12))
        forecast_label.pack()
        self.forecast_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.forecast_entry.pack()

        # Buttons
        add_button = tk.Button(self.root, text="Add Forecast", command=self.add_forecast, width=20, font=("Arial", 12))
        add_button.pack(pady=5)

        view_button = tk.Button(self.root, text="View Forecast", command=self.view_forecast, width=20, font=("Arial", 12))
        view_button.pack(pady=5)

        update_button = tk.Button(self.root, text="Update Forecast", command=self.update_forecast, width=20, font=("Arial", 12))
        update_button.pack(pady=5)

        remove_button = tk.Button(self.root, text="Remove Forecast", command=self.remove_forecast, width=20, font=("Arial", 12))
        remove_button.pack(pady=5)

        # Output Area
        output_label = tk.Label(self.root, text="Output:", font=("Arial", 12, "bold"))
        output_label.pack(pady=10)
        self.output_text = tk.Text(self.root, height=10, width=50, font=("Arial", 10))
        self.output_text.pack()

    def add_forecast(self):
        city = self.city_entry.get().strip()
        forecast = self.forecast_entry.get().strip()

        if not city or not forecast:
            messagebox.showerror("Input Error", "City and Forecast fields cannot be empty!")
            return

        self.city_forecasts[city] = forecast
        self.output_text.insert(tk.END, f"Added forecast for {city}: {forecast}\n")
        self.clear_inputs()

    def view_forecast(self):
        city = self.city_entry.get().strip()

        if not city:
            messagebox.showerror("Input Error", "City field cannot be empty!")
            return

        if city in self.city_forecasts:
            forecast = self.city_forecasts[city]
            self.output_text.insert(tk.END, f"Weather forecast for {city}: {forecast}\n")
        else:
            self.output_text.insert(tk.END, f"No forecast data available for {city}.\n")
        self.clear_inputs()

    def update_forecast(self):
        city = self.city_entry.get().strip()
        new_forecast = self.forecast_entry.get().strip()

        if not city or not new_forecast:
            messagebox.showerror("Input Error", "City and Forecast fields cannot be empty!")
            return

        if city in self.city_forecasts:
            self.city_forecasts[city] = new_forecast
            self.output_text.insert(tk.END, f"Weather forecast for {city} updated to: {new_forecast}\n")
        else:
            self.output_text.insert(tk.END, f"No forecast data found for {city} to update.\n")
        self.clear_inputs()

    def remove_forecast(self):
        city = self.city_entry.get().strip()

        if not city:
            messagebox.showerror("Input Error", "City field cannot be empty!")
            return

        if city in self.city_forecasts:
            del self.city_forecasts[city]
            self.output_text.insert(tk.END, f"Weather forecast for {city} removed.\n")
        else:
            self.output_text.insert(tk.END, f"No forecast data found for {city} to remove.\n")
        self.clear_inputs()

    def clear_inputs(self):
        """Clear the input fields."""
        self.city_entry.delete(0, tk.END)
        self.forecast_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherForecastingTool(root)
    root.mainloop()

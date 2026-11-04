import tkinter as tk
from tkinter import messagebox
import datetime


class HabitTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker with Health Options")
        self.root.geometry("700x500")
        self.habits = {}

        # Title
        tk.Label(root, text="Habit Tracker with Health Options", font=("Arial", 20, "bold")).pack(pady=10)

        # Habit Listbox
        self.habit_listbox = tk.Listbox(root, font=("Arial", 12), width=40, height=10)
        self.habit_listbox.pack(pady=10)
        self.habit_listbox.bind("<<ListboxSelect>>", self.show_habit_details)

        # Add Habit Section
        self.add_habit_frame = tk.Frame(root)
        self.add_habit_frame.pack(pady=10)

        tk.Label(self.add_habit_frame, text="Habit Name:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.habit_name_entry = tk.Entry(self.add_habit_frame, font=("Arial", 12), width=20)
        self.habit_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.add_habit_frame, text="Goal (e.g., daily):", font=("Arial", 12)).grid(row=0, column=2, padx=5, pady=5)
        self.habit_goal_entry = tk.Entry(self.add_habit_frame, font=("Arial", 12), width=20)
        self.habit_goal_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(self.add_habit_frame, text="Add Habit", font=("Arial", 12), command=self.add_habit).grid(row=0, column=4, padx=5, pady=5)

        # Health Tracking Section
        self.health_frame = tk.LabelFrame(root, text="Health Tracking", font=("Arial", 14, "bold"), padx=10, pady=10)
        self.health_frame.pack(pady=10)

        tk.Label(self.health_frame, text="Steps:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.steps_entry = tk.Entry(self.health_frame, font=("Arial", 12), width=10)
        self.steps_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.health_frame, text="Water (ml):", font=("Arial", 12)).grid(row=0, column=2, padx=5, pady=5)
        self.water_entry = tk.Entry(self.health_frame, font=("Arial", 12), width=10)
        self.water_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.health_frame, text="Sleep (hrs):", font=("Arial", 12)).grid(row=0, column=4, padx=5, pady=5)
        self.sleep_entry = tk.Entry(self.health_frame, font=("Arial", 12), width=10)
        self.sleep_entry.grid(row=0, column=5, padx=5, pady=5)

        tk.Button(self.health_frame, text="Record Health", font=("Arial", 12), command=self.record_health).grid(row=0, column=6, padx=5, pady=5)
        tk.Button(self.health_frame, text="View Health Stats", font=("Arial", 12), command=self.view_health_stats).grid(row=1, columnspan=7, pady=5)

        # Action Buttons
        self.action_frame = tk.Frame(root)
        self.action_frame.pack(pady=10)

        tk.Button(self.action_frame, text="Record Completion", font=("Arial", 12), command=self.record_completion).grid(row=0, column=0, padx=5)
        tk.Button(self.action_frame, text="View Progress", font=("Arial", 12), command=self.view_progress).grid(row=0, column=1, padx=5)
        tk.Button(self.action_frame, text="Delete Habit", font=("Arial", 12), command=self.delete_habit).grid(row=0, column=2, padx=5)

    def add_habit(self):
        """Add a new habit."""
        name = self.habit_name_entry.get().strip()
        goal = self.habit_goal_entry.get().strip()

        if name and goal:
            if name in self.habits:
                messagebox.showwarning("Warning", f"Habit '{name}' already exists!")
            else:
                self.habits[name] = {"goal": goal, "completed_dates": set()}
                self.habit_listbox.insert(tk.END, name)
                self.habit_name_entry.delete(0, tk.END)
                self.habit_goal_entry.delete(0, tk.END)
                messagebox.showinfo("Success", f"Habit '{name}' added!")
        else:
            messagebox.showwarning("Warning", "Please provide both a habit name and a goal.")

    def record_completion(self):
        """Record today's completion for the selected habit."""
        selected_habit = self.get_selected_habit()
        if selected_habit:
            today = datetime.date.today()
            self.habits[selected_habit]["completed_dates"].add(today)
            messagebox.showinfo("Success", f"Marked '{selected_habit}' as completed for today.")
        else:
            messagebox.showwarning("Warning", "Please select a habit to record.")

    def view_progress(self):
        """View the progress and streak for the selected habit."""
        selected_habit = self.get_selected_habit()
        if selected_habit:
            completed_dates = self.habits[selected_habit]["completed_dates"]
            if completed_dates:
                streak = self.calculate_streak(completed_dates)
                total_days = (datetime.date.today() - min(completed_dates)).days + 1
                progress = (len(completed_dates) / total_days) * 100 if total_days > 0 else 0

                message = (
                    f"Habit: {selected_habit}\n"
                    f"Goal: {self.habits[selected_habit]['goal']}\n"
                    f"Progress: {progress:.2f}%\n"
                    f"Total Days Completed: {len(completed_dates)}\n"
                    f"Current Streak: {streak} day(s)"
                )
                messagebox.showinfo("Progress", message)
            else:
                messagebox.showinfo("Progress", f"No completions recorded for '{selected_habit}'.")
        else:
            messagebox.showwarning("Warning", "Please select a habit to view progress.")

    def delete_habit(self):
        """Delete the selected habit."""
        selected_habit = self.get_selected_habit()
        if selected_habit:
            del self.habits[selected_habit]
            self.habit_listbox.delete(self.habit_listbox.curselection())
            messagebox.showinfo("Success", f"Habit '{selected_habit}' deleted!")
        else:
            messagebox.showwarning("Warning", "Please select a habit to delete.")

    def calculate_streak(self, completed_dates):
        """Calculate the current streak of consecutive completions."""
        if not completed_dates:
            return 0
        sorted_dates = sorted(completed_dates, reverse=True)
        streak = 1
        for i in range(1, len(sorted_dates)):
            if sorted_dates[i] == sorted_dates[i - 1] - datetime.timedelta(days=1):
                streak += 1
            else:
                break
        return streak

    def record_health(self):
        """Record health metrics."""
        try:
            steps = int(self.steps_entry.get().strip())
            water = int(self.water_entry.get().strip())
            sleep = float(self.sleep_entry.get().strip())
        except ValueError:
            messagebox.showwarning("Warning", "Please enter valid numeric values for health metrics.")
            return

        if "Health" not in self.habits:
            self.habits["Health"] = {"steps": [], "water": [], "sleep": []}

        today = datetime.date.today()
        self.habits["Health"]["steps"].append((today, steps))
        self.habits["Health"]["water"].append((today, water))
        self.habits["Health"]["sleep"].append((today, sleep))

        self.steps_entry.delete(0, tk.END)
        self.water_entry.delete(0, tk.END)
        self.sleep_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Health metrics recorded successfully!")

    def view_health_stats(self):
        """View health statistics."""
        if "Health" in self.habits:
            health = self.habits["Health"]
            steps = [s[1] for s in health["steps"]]
            water = [w[1] for w in health["water"]]
            sleep = [s[1] for s in health["sleep"]]

            avg_steps = sum(steps) / len(steps) if steps else 0
            avg_water = sum(water) / len(water) if water else 0
            avg_sleep = sum(sleep) / len(sleep) if sleep else 0

            message = (
                f"Health Statistics:\n\n"
                f"Average Steps: {avg_steps:.2f}\n"
                f"Average Water Intake: {avg_water:.2f} ml\n"
                f"Average Sleep: {avg_sleep:.2f} hours"
            )
            messagebox.showinfo("Health Stats", message)
        else:
            messagebox.showwarning("Warning", "No health data recorded yet.")

    def get_selected_habit(self):
        """Get the currently selected habit from the listbox."""
        selected = self.habit_listbox.curselection()
        if selected:
            return self.habit_listbox.get(selected[0])
        return None

    def show_habit_details(self, event):
        """Display details about the selected habit."""
        selected_habit = self.get_selected_habit()
        if selected_habit:
            goal = self.habits[selected_habit]["goal"]
            messagebox.showinfo("Habit Details", f"Habit: {selected_habit}\nGoal: {goal}")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerGUI(root)
    root.mainloop()

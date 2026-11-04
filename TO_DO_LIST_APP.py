import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import csv

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.tasks = {}
        self.task_counter = 1  # To generate unique task IDs

        # Default theme is Light
        self.dark_mode = False

        # Widgets for input
        tk.Label(root, text="Task:").pack(pady=5)
        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=5)

        tk.Label(root, text="Due Date (YYYY-MM-DD, optional):").pack(pady=5)
        self.due_date_entry = tk.Entry(root, width=20)
        self.due_date_entry.pack(pady=5)

        # Priority Input
        tk.Label(root, text="Priority (Low, Medium, High):").pack(pady=5)
        self.priority_entry = tk.Entry(root, width=20)
        self.priority_entry.pack(pady=5)

        # Buttons
        tk.Button(root, text="Add Task", command=self.add_task).pack(pady=5)
        tk.Button(root, text="View Tasks", command=self.list_tasks).pack(pady=5)
        tk.Button(root, text="Show Tasks Due Today", command=self.show_due_today).pack(pady=5)
        tk.Button(root, text="Remove Task", command=self.remove_task).pack(pady=5)
        tk.Button(root, text="Export Tasks to CSV", command=self.export_tasks).pack(pady=5)
        tk.Button(root, text="Toggle Dark Mode", command=self.toggle_dark_mode).pack(pady=5)
        tk.Button(root, text="Mark Task as Completed", command=self.mark_task_completed).pack(pady=5)

        # Output box
        self.output_label = tk.Label(root, text="", justify="left", wraplength=400)
        self.output_label.pack(pady=10)

    def add_task(self):
        """Add a new task to the list."""
        task = self.task_entry.get().strip()
        due_date = self.due_date_entry.get().strip()
        priority = self.priority_entry.get().strip()
        if not task:
            messagebox.showerror("Error", "Task description cannot be empty!")
            return

        if priority not in ["Low", "Medium", "High"]:
            messagebox.showerror("Error", "Please enter a valid priority (Low, Medium, High).")
            return

        try:
            if due_date:
                due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
            else:
                due_date = None
            task_id = self.task_counter
            self.tasks[task_id] = {"task": task, "due_date": due_date, "priority": priority, "status": "Pending"}
            self.task_counter += 1
            self.task_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            self.output_label.config(text=f"Task added: {task} (ID: {task_id}, Due: {due_date or 'No due date'}, Priority: {priority})")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")

    def list_tasks(self):
        """List all tasks with their due dates, priorities, and statuses."""
        if not self.tasks:
            self.output_label.config(text="No tasks in the list.")
            return

        output = "To-Do List:\n"
        for task_id, task_info in self.tasks.items():
            task = task_info["task"]
            due_date = task_info["due_date"] if task_info["due_date"] else "No due date"
            priority = task_info["priority"]
            status = task_info["status"]
            output += f"Task ID: {task_id}, Task: {task}, Due Date: {due_date}, Priority: {priority}, Status: {status}\n"
        self.output_label.config(text=output)

    def show_due_today(self):
        """Show tasks that are due today."""
        today = datetime.date.today()
        due_today = [
            (task_id, task_info["task"], task_info["priority"]) 
            for task_id, task_info in self.tasks.items() 
            if task_info["due_date"] == today
        ]

        if due_today:
            output = "Tasks due today:\n"
            for task_id, task, priority in due_today:
                output += f"Task ID: {task_id}, Task: {task}, Priority: {priority}\n"
            self.output_label.config(text=output)
        else:
            self.output_label.config(text="No tasks are due today.")

    def remove_task(self):
        """Remove a task by its task ID."""
        task_id = self.task_entry.get().strip()
        if not task_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric Task ID!")
            return

        task_id = int(task_id)
        if task_id in self.tasks:
            removed_task = self.tasks.pop(task_id)
            self.output_label.config(text=f"Task removed: {removed_task['task']}")
            self.task_entry.delete(0, tk.END)
        else:
            self.output_label.config(text=f"Task with ID {task_id} not found.")

    def export_tasks(self):
        """Export tasks to a CSV file."""
        if not self.tasks:
            messagebox.showerror("Error", "No tasks to export.")
            return

        with open("tasks.csv", "w", newline="") as csvfile:
            fieldnames = ["Task ID", "Task", "Due Date", "Priority", "Status"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for task_id, task_info in self.tasks.items():
                writer.writerow({
                    "Task ID": task_id,
                    "Task": task_info["task"],
                    "Due Date": task_info["due_date"] if task_info["due_date"] else "No due date",
                    "Priority": task_info["priority"],
                    "Status": task_info["status"]
                })
        messagebox.showinfo("Success", "Tasks exported to tasks.csv.")

    def mark_task_completed(self):
        """Mark a task as completed."""
        task_id = self.task_entry.get().strip()
        if not task_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid Task ID!")
            return

        task_id = int(task_id)
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = "Completed"
            self.output_label.config(text=f"Task ID {task_id} marked as completed.")
            self.task_entry.delete(0, tk.END)
        else:
            self.output_label.config(text=f"Task with ID {task_id} not found.")

    def toggle_dark_mode(self):
        """Toggle between dark and light mode."""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.root.config(bg="black")
            self.output_label.config(bg="black", fg="white")
            self.task_entry.config(bg="black", fg="white")
            self.due_date_entry.config(bg="black", fg="white")
            self.priority_entry.config(bg="black", fg="white")
        else:
            self.root.config(bg="white")
            self.output_label.config(bg="white", fg="black")
            self.task_entry.config(bg="white", fg="black")
            self.due_date_entry.config(bg="white", fg="black")
            self.priority_entry.config(bg="white", fg="black")


# Create the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()

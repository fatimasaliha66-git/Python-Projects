import tkinter as tk
from tkinter import messagebox
import csv
import matplotlib.pyplot as plt
from tkinter import simpledialog

class StudentGradeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Management System")
        self.students = {}

        # Widgets for adding a student
        tk.Label(root, text="Student Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Grade:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.grade_entry = tk.Entry(root)
        self.grade_entry.grid(row=1, column=1, padx=10, pady=5)

        # Widgets for student profile (optional details)
        tk.Label(root, text="Age (optional):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.age_entry = tk.Entry(root)
        self.age_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Gender (optional):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.gender_entry = tk.Entry(root)
        self.gender_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons for managing students and grades
        tk.Button(root, text="Add Student", command=self.add_student).grid(row=4, column=0, padx=10, pady=10)
        tk.Button(root, text="Remove Student", command=self.remove_student).grid(row=4, column=1, padx=10, pady=10)
        tk.Button(root, text="Update Grade", command=self.update_grade).grid(row=5, column=0, padx=10, pady=10)
        tk.Button(root, text="Get Grade", command=self.get_student_grade).grid(row=5, column=1, padx=10, pady=10)

        # Buttons for grade statistics and export
        tk.Button(root, text="Average Grade", command=self.get_average_grade).grid(row=6, column=0, padx=10, pady=10)
        tk.Button(root, text="Highest Grade", command=self.get_highest_grade).grid(row=6, column=1, padx=10, pady=10)
        tk.Button(root, text="Lowest Grade", command=self.get_lowest_grade).grid(row=7, column=0, padx=10, pady=10)
        tk.Button(root, text="Export Grades to CSV", command=self.export_grades).grid(row=7, column=1, padx=10, pady=10)

        # Buttons for visualization and search
        tk.Button(root, text="Visualize Grades", command=self.visualize_grades).grid(row=8, column=0, padx=10, pady=10)
        tk.Button(root, text="Search Student", command=self.search_student).grid(row=8, column=1, padx=10, pady=10)

        # Output area
        self.output_label = tk.Label(root, text="", justify="left", wraplength=400, fg="blue")
        self.output_label.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    def add_student(self):
        """Add a student and their grade to the system."""
        name = self.name_entry.get().strip()
        grade = self.grade_entry.get().strip()
        age = self.age_entry.get().strip()
        gender = self.gender_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Student name cannot be empty!")
            return
        if not grade.isdigit():
            messagebox.showerror("Error", "Grade must be a valid number!")
            return

        # Store optional details
        student_info = {
            "grade": int(grade),
            "age": age if age else "Not provided",
            "gender": gender if gender else "Not provided"
        }
        self.students[name] = student_info
        self.name_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.gender_entry.delete(0, tk.END)
        self.output_label.config(text=f"Student {name} added with grade {grade}.")

    def remove_student(self):
        """Remove a student from the system."""
        name = self.name_entry.get().strip()
        if name in self.students:
            del self.students[name]
            self.output_label.config(text=f"Student {name} removed.")
        else:
            self.output_label.config(text=f"Student {name} not found.")

    def update_grade(self):
        """Update the grade of a student."""
        name = self.name_entry.get().strip()
        if name in self.students:
            new_grade = simpledialog.askinteger("Update Grade", f"Enter new grade for {name}:")
            if new_grade is not None:
                self.students[name]["grade"] = new_grade
                self.output_label.config(text=f"Grade for {name} updated to {new_grade}.")
            else:
                self.output_label.config(text="Invalid grade entered.")
        else:
            self.output_label.config(text=f"Student {name} not found.")

    def get_student_grade(self):
        """Get the grade of a specific student."""
        name = self.name_entry.get().strip()
        if name in self.students:
            grade = self.students[name]["grade"]
            self.output_label.config(text=f"Student {name}'s grade: {grade}.")
        else:
            self.output_label.config(text="Student not found.")

    def get_average_grade(self):
        """Calculate the average grade of all students."""
        if not self.students:
            self.output_label.config(text="No students in the system.")
            return

        total_grades = sum(student["grade"] for student in self.students.values())
        average_grade = total_grades / len(self.students)
        self.output_label.config(text=f"Average Grade: {round(average_grade, 2)}.")

    def get_highest_grade(self):
        """Get the highest grade in the class."""
        if not self.students:
            self.output_label.config(text="No students in the system.")
            return

        highest_grade = max(student["grade"] for student in self.students.values())
        self.output_label.config(text=f"Highest Grade: {highest_grade}.")

    def get_lowest_grade(self):
        """Get the lowest grade in the class."""
        if not self.students:
            self.output_label.config(text="No students in the system.")
            return

        lowest_grade = min(student["grade"] for student in self.students.values())
        self.output_label.config(text=f"Lowest Grade: {lowest_grade}.")

    def view_all_grades(self):
        """Display all students and their grades."""
        if not self.students:
            self.output_label.config(text="No students in the system.")
            return

        output = "All Students and Grades:\n"
        for name, details in self.students.items():
            output += f"{name}: Grade: {details['grade']}, Age: {details['age']}, Gender: {details['gender']}\n"
        self.output_label.config(text=output)

    def export_grades(self):
        """Export grades to a CSV file."""
        if not self.students:
            messagebox.showerror("Error", "No students to export.")
            return

        with open("student_grades.csv", "w", newline="") as csvfile:
            fieldnames = ["Student Name", "Grade", "Age", "Gender"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for name, details in self.students.items():
                writer.writerow({
                    "Student Name": name,
                    "Grade": details["grade"],
                    "Age": details["age"],
                    "Gender": details["gender"]
                })
        messagebox.showinfo("Success", "Student grades exported to student_grades.csv.")

    def visualize_grades(self):
        """Visualize student grades with a bar chart."""
        if not self.students:
            messagebox.showerror("Error", "No students to visualize.")
            return

        names = list(self.students.keys())
        grades = [details["grade"] for details in self.students.values()]

        plt.bar(names, grades, color='blue')
        plt.xlabel("Students")
        plt.ylabel("Grades")
        plt.title("Student Grades")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def search_student(self):
        """Search for a student by name."""
        name = self.name_entry.get().strip()
        if name in self.students:
            details = self.students[name]
            self.output_label.config(text=f"Student {name}: Grade: {details['grade']}, Age: {details['age']}, Gender: {details['gender']}")
        else:
            self.output_label.config(text="Student not found.")

# Create the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentGradeManagementSystem(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox
import random
import time


class QuizAppGUI:
    def __init__(self, root):
        # Initialize the quiz data
        self.questions = {
            "What is the capital of France?": ["paris", "A. Paris", "B. London", "C. Rome", "D. Berlin"],
            "What is 2 + 2?": ["4", "A. 3", "B. 4", "C. 5", "D. 6"],
            "What is the color of the sky?": ["blue", "A. Blue", "B. Green", "C. Red", "D. Yellow"],
            "What is the largest planet in our solar system?": ["jupiter", "A. Mars", "B. Earth", "C. Jupiter", "D. Saturn"],
        }
        self.current_question_index = 0
        self.score = 0
        self.start_time = None
        self.time_left = 15  # seconds per question
        self.timer_running = False

        # Convert questions to a list for indexing
        self.question_list = list(self.questions.keys())
        self.total_questions = len(self.questions)

        # Shuffle the questions for randomization
        random.shuffle(self.question_list)

        # Configure the window
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        # Create the GUI layout
        # Score
        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(anchor="nw", padx=10, pady=5)

        # Question Display
        self.question_label = tk.Label(
            root, text="", font=("Arial", 16), wraplength=400, justify="center"
        )
        self.question_label.pack(pady=20)

        # Timer Label
        self.timer_label = tk.Label(root, text="Time Left: 15s", font=("Arial", 12))
        self.timer_label.pack(pady=5)

        # Multiple Choice Options
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(root, text="", font=("Arial", 12), width=30, command=lambda i=i: self.submit_answer(i))
            btn.pack(pady=5)
            self.option_buttons.append(btn)

        # Feedback
        self.feedback_label = tk.Label(root, text="", font=("Arial", 14))
        self.feedback_label.pack(pady=10)

        # Progress Bar
        self.progress_bar = tk.Label(root, text="", font=("Arial", 12), width=30)
        self.progress_bar.pack(pady=10)

        # Start the first question
        self.show_question()

    def show_question(self):
        """Display the next question."""
        if self.current_question_index < self.total_questions:
            question = self.question_list[self.current_question_index]
            self.question_label.config(text=question)

            # Display the multiple choice options
            correct_answer = self.questions[question][0]
            random.shuffle(self.questions[question][1:])  # Shuffle options
            for i, btn in enumerate(self.option_buttons):
                btn.config(text=self.questions[question][i + 1])

            # Reset feedback and start timer
            self.feedback_label.config(text="")
            self.time_left = 15
            self.start_timer()
            self.update_progress_bar()

        else:
            self.end_quiz()

    def start_timer(self):
        """Start the timer for the current question."""
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        """Update the timer countdown every second."""
        elapsed_time = time.time() - self.start_time
        remaining_time = self.time_left - int(elapsed_time)

        if remaining_time >= 0:
            self.timer_label.config(text=f"Time Left: {remaining_time}s")
            self.root.after(1000, self.update_timer)  # Update every second
        else:
            self.submit_answer(-1)  # Automatically submit if time is up

    def submit_answer(self, selected_option):
        """Check the user's answer and update the score."""
        correct_answer = self.questions[self.question_list[self.current_question_index]][0]
        if selected_option == -1:
            self.feedback_label.config(text=f"Time's up! The correct answer was '{correct_answer}'.", fg="red")
        else:
            user_answer = self.option_buttons[selected_option].cget("text")[3:].strip().lower()
            if user_answer == correct_answer:
                self.feedback_label.config(text="Correct!", fg="green")
                self.score += 1
            else:
                self.feedback_label.config(text=f"Incorrect! The correct answer was '{correct_answer}'.", fg="red")

        # Move to the next question
        self.current_question_index += 1
        self.root.after(2000, self.show_question)

    def update_progress_bar(self):
        """Update the progress bar based on the number of questions answered."""
        progress = int((self.current_question_index / self.total_questions) * 100)
        self.progress_bar.config(text=f"Progress: {progress}%")

    def show_hint(self):
        """Display a hint for the current question."""
        if self.current_question_index < self.total_questions:
            question = self.question_list[self.current_question_index]
            correct_answer = self.questions[question][0]
            hint = correct_answer[0] + ("*" * (len(correct_answer) - 1))
            messagebox.showinfo("Hint", f"The answer starts with: {hint}")

    def end_quiz(self):
        """End the quiz and display the final score."""
        messagebox.showinfo(
            "Quiz Completed",
            f"You've completed the quiz!\nFinal Score: {self.score}/{self.total_questions}",
        )
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizAppGUI(root)
    root.mainloop()

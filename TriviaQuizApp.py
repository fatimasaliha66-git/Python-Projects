import random
import tkinter as tk
from tkinter import ttk, messagebox

class TriviaQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Trivia Quiz Generator")

        # Question pool with difficulty levels
        self.questions = {
            "easy": [],
            "medium": [],
            "hard": []
        }
        
        # Initialize score
        self.score = 0
        self.total_questions = 0

        # Create the GUI
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title_label = ttk.Label(self.root, text="Random Trivia Quiz Generator", font=("Arial", 20))
        self.title_label.pack(pady=10)

        # Add Question Button
        self.add_question_button = ttk.Button(self.root, text="Add Question", command=self.add_question_window)
        self.add_question_button.pack(pady=5)

        # Start Quiz Button
        self.start_quiz_button = ttk.Button(self.root, text="Start Quiz", command=self.start_quiz)
        self.start_quiz_button.pack(pady=5)

        # Difficulty Level ComboBox
        self.difficulty_label = ttk.Label(self.root, text="Select Difficulty:")
        self.difficulty_label.pack(pady=5)

        self.difficulty_combobox = ttk.Combobox(self.root, values=["easy", "medium", "hard"], state="readonly")
        self.difficulty_combobox.set("easy")
        self.difficulty_combobox.pack(pady=5)

        # Score Display
        self.score_label = ttk.Label(self.root, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(pady=10)

    def add_question_window(self):
        # New window to add a question
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Question")

        # Question Label and Entry
        question_label = ttk.Label(add_window, text="Enter Question:")
        question_label.pack(pady=5)
        question_entry = ttk.Entry(add_window, width=40)
        question_entry.pack(pady=5)

        # Answer Label and Entry
        answer_label = ttk.Label(add_window, text="Enter Correct Answer:")
        answer_label.pack(pady=5)
        answer_entry = ttk.Entry(add_window, width=40)
        answer_entry.pack(pady=5)

        # Difficulty Label and ComboBox
        difficulty_label = ttk.Label(add_window, text="Select Difficulty:")
        difficulty_label.pack(pady=5)
        difficulty_combobox = ttk.Combobox(add_window, values=["easy", "medium", "hard"], state="readonly")
        difficulty_combobox.set("easy")
        difficulty_combobox.pack(pady=5)

        # Add Question Button
        add_button = ttk.Button(add_window, text="Add Question", command=lambda: self.add_question(
            question_entry.get(), answer_entry.get(), difficulty_combobox.get(), add_window))
        add_button.pack(pady=5)

    def add_question(self, question, answer, difficulty, window):
        if not question or not answer:
            messagebox.showerror("Error", "Question and Answer cannot be empty!")
            return

        self.questions[difficulty].append({"question": question, "answer": answer})
        messagebox.showinfo("Success", "Question Added Successfully!")
        window.destroy()

    def start_quiz(self):
        # Get the selected difficulty
        difficulty = self.difficulty_combobox.get()

        if not self.questions[difficulty]:
            messagebox.showerror("No Questions", f"No {difficulty} questions available.")
            return

        # Reset score
        self.score = 0
        self.total_questions = 0
        self.ask_question(difficulty)

    def ask_question(self, difficulty):
        # Select a random question from the pool
        question_data = random.choice(self.questions[difficulty])
        question = question_data["question"]
        correct_answer = question_data["answer"]

        # Increment total questions
        self.total_questions += 1

        # Ask the question
        answer = self.ask_question_window(question)
        self.check_answer(answer, correct_answer, difficulty)

    def ask_question_window(self, question):
        # Display question and get answer
        answer_window = tk.Toplevel(self.root)
        answer_window.title("Answer Question")

        question_label = ttk.Label(answer_window, text=question, font=("Arial", 14))
        question_label.pack(pady=10)

        answer_entry = ttk.Entry(answer_window, width=40)
        answer_entry.pack(pady=5)

        submit_button = ttk.Button(answer_window, text="Submit", command=lambda: answer_window.destroy())
        submit_button.pack(pady=5)

        self.root.wait_window(answer_window)  # Wait until window is closed
        return answer_entry.get()

    def check_answer(self, user_answer, correct_answer, difficulty):
        # Check answer and update score
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            messagebox.showinfo("Correct!", "Your answer is correct!")
        else:
            messagebox.showerror("Incorrect", f"The correct answer was: {correct_answer}")

        # Update score display
        self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")

        # Ask next question or finish quiz
        if self.total_questions < 5:  # Limit quiz to 5 questions for simplicity
            self.ask_question(difficulty)
        else:
            messagebox.showinfo("Quiz Over", f"Quiz over! Your final score is {self.score}/{self.total_questions}.")

# Initialize the application
root = tk.Tk()
app = TriviaQuizApp(root)

# Start the main loop
root.mainloop()

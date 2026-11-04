import tkinter as tk
from tkinter import ttk, messagebox
import random
import json

# Functions
def add_flashcard():
    question = question_entry.get()
    answer = answer_entry.get()
    category = category_combobox.get()
    if not question or not answer or not category:
        messagebox.showerror("Error", "All fields are required.")
        return
    flashcard = {'question': question, 'answer': answer, 'category': category}
    flashcards.append(flashcard)
    save_flashcards()
    question_entry.delete(0, tk.END)
    answer_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Flashcard added!")

def practice_flashcards(shuffle=False):
    global current_card
    if not flashcards:
        messagebox.showinfo("No Flashcards", "Please add flashcards first.")
        return
    if shuffle:
        random.shuffle(flashcards)
    current_card = random.choice(flashcards)
    question_label.config(text=f"Category: {current_card['category']}\n{current_card['question']}")
    answer_entry_practice.delete(0, tk.END)
    practice_frame.pack()
    main_menu.pack_forget()

def check_answer():
    global correct_count, total_count
    user_answer = answer_entry_practice.get()
    if not user_answer:
        messagebox.showerror("Error", "Please enter an answer.")
        return
    total_count += 1
    if user_answer.lower() == current_card['answer'].lower():
        correct_count += 1
        messagebox.showinfo("Correct!", "Your answer is correct!")
    else:
        messagebox.showerror("Incorrect", f"Correct answer: {current_card['answer']}")
    update_progress()
    practice_flashcards()

def update_progress():
    progress_label.config(text=f"Correct: {correct_count}, Total: {total_count}")

def reset_progress():
    global correct_count, total_count
    correct_count = 0
    total_count = 0
    update_progress()
    messagebox.showinfo("Reset", "Progress has been reset.")

def save_flashcards():
    with open("flashcards.json", "w") as file:
        json.dump(flashcards, file)

def load_flashcards():
    global flashcards
    try:
        with open("flashcards.json", "r") as file:
            flashcards = json.load(file)
    except FileNotFoundError:
        flashcards = []

def view_flashcards():
    view_window = tk.Toplevel(root)
    view_window.title("View Flashcards")
    view_frame = ttk.Frame(view_window, padding="10")
    view_frame.pack()
    
    for i, card in enumerate(flashcards):
        ttk.Label(view_frame, text=f"{i+1}. {card['category']} - {card['question']}").pack(anchor=tk.W)
    
    ttk.Button(view_frame, text="Close", command=view_window.destroy).pack(pady=5)

def remove_flashcard():
    remove_window = tk.Toplevel(root)
    remove_window.title("Remove Flashcard")
    remove_frame = ttk.Frame(remove_window, padding="10")
    remove_frame.pack()
    
    flashcard_listbox = tk.Listbox(remove_frame, width=50, height=10)
    flashcard_listbox.pack()
    
    for i, card in enumerate(flashcards):
        flashcard_listbox.insert(tk.END, f"{i+1}. {card['category']} - {card['question']}")
    
    def delete_selected():
        selected = flashcard_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a flashcard to remove.")
            return
        index = selected[0]
        del flashcards[index]
        save_flashcards()
        messagebox.showinfo("Success", "Flashcard removed!")
        remove_window.destroy()
    
    ttk.Button(remove_frame, text="Delete", command=delete_selected).pack(pady=5)
    ttk.Button(remove_frame, text="Close", command=remove_window.destroy).pack(pady=5)

# Initialize App
root = tk.Tk()
root.title("Flashcard App")

flashcards = []
current_card = None
correct_count = 0
total_count = 0

# Load existing flashcards
load_flashcards()

# Main Menu
main_menu = ttk.Frame(root, padding="10")
main_menu.pack()

ttk.Button(main_menu, text="Add Flashcard", command=lambda: add_flashcard_frame.pack()).pack(pady=5)
ttk.Button(main_menu, text="Practice Flashcards", command=lambda: practice_flashcards(shuffle=False)).pack(pady=5)
ttk.Button(main_menu, text="Practice (Shuffle)", command=lambda: practice_flashcards(shuffle=True)).pack(pady=5)
ttk.Button(main_menu, text="View Flashcards", command=view_flashcards).pack(pady=5)
ttk.Button(main_menu, text="Remove Flashcard", command=remove_flashcard).pack(pady=5)
ttk.Button(main_menu, text="Reset Progress", command=reset_progress).pack(pady=5)
progress_label = ttk.Label(main_menu, text="Correct: 0, Total: 0")
progress_label.pack(pady=5)

# Add Flashcard Frame
add_flashcard_frame = ttk.Frame(root, padding="10")
ttk.Label(add_flashcard_frame, text="Add Flashcard").pack(pady=5)
ttk.Label(add_flashcard_frame, text="Question:").pack(anchor=tk.W)
question_entry = ttk.Entry(add_flashcard_frame, width=40)
question_entry.pack()
ttk.Label(add_flashcard_frame, text="Answer:").pack(anchor=tk.W)
answer_entry = ttk.Entry(add_flashcard_frame, width=40)
answer_entry.pack()
ttk.Label(add_flashcard_frame, text="Category:").pack(anchor=tk.W)
category_combobox = ttk.Combobox(add_flashcard_frame, values=["Science", "Math", "History", "Other"])
category_combobox.pack()
ttk.Button(add_flashcard_frame, text="Add", command=add_flashcard).pack(pady=5)
ttk.Button(add_flashcard_frame, text="Back to Menu", command=lambda: [add_flashcard_frame.pack_forget(), main_menu.pack()]).pack()

# Practice Flashcard Frame
practice_frame = ttk.Frame(root, padding="10")
question_label = ttk.Label(practice_frame, text="", wraplength=300)
question_label.pack(pady=5)
ttk.Label(practice_frame, text="Your Answer:").pack(anchor=tk.W)
answer_entry_practice = ttk.Entry(practice_frame, width=40)
answer_entry_practice.pack()
ttk.Button(practice_frame, text="Submit", command=check_answer).pack(pady=5)
ttk.Button(practice_frame, text="Back to Menu", command=lambda: [practice_frame.pack_forget(), main_menu.pack()]).pack()

# Start App
root.mainloop()

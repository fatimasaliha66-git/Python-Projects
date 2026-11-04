import tkinter as tk
from tkinter import messagebox
import csv
import os


class SocialMediaPostManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Media Post Manager")
        self.root.geometry("600x500")
        self.posts = {}
        self.post_counter = 1  # Unique post ID counter
        self.tags_history = set()  # Store previously used tags for auto-completion

        # Title
        self.title_label = tk.Label(root, text="Social Media Post Manager", font=("Arial", 20))
        self.title_label.pack(pady=10)

        # Post List
        self.post_listbox = tk.Listbox(root, font=("Arial", 14), height=10, width=50)
        self.post_listbox.pack(pady=10)
        self.post_listbox.bind("<<ListboxSelect>>", self.show_post_details)

        # Search Bar
        self.search_label = tk.Label(root, text="Search Posts:", font=("Arial", 12))
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(root, font=("Arial", 12))
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_posts)

        # Add Post Section
        self.add_post_frame = tk.Frame(root)
        self.add_post_frame.pack(pady=10)

        self.add_post_label = tk.Label(self.add_post_frame, text="Post Content:", font=("Arial", 12))
        self.add_post_label.grid(row=0, column=0, padx=5)
        self.add_post_entry = tk.Entry(self.add_post_frame, font=("Arial", 12), width=30)
        self.add_post_entry.grid(row=0, column=1, padx=5)
        self.add_tags_label = tk.Label(self.add_post_frame, text="Tags (comma-separated):", font=("Arial", 12))
        self.add_tags_label.grid(row=1, column=0, padx=5)
        self.add_tags_entry = tk.Entry(self.add_post_frame, font=("Arial", 12), width=30)
        self.add_tags_entry.grid(row=1, column=1, padx=5)
        self.add_post_button = tk.Button(self.add_post_frame, text="Add Post", font=("Arial", 12), command=self.add_post)
        self.add_post_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Buttons for Actions
        self.action_frame = tk.Frame(root)
        self.action_frame.pack(pady=10)

        self.delete_button = tk.Button(self.action_frame, text="Delete Selected Post", font=("Arial", 12), command=self.delete_post)
        self.delete_button.grid(row=0, column=0, padx=5)

        self.view_posts_button = tk.Button(self.action_frame, text="Refresh Posts", font=("Arial", 12), command=self.view_posts)
        self.view_posts_button.grid(row=0, column=1, padx=5)

        self.edit_button = tk.Button(self.action_frame, text="Edit Selected Post", font=("Arial", 12), command=self.edit_post)
        self.edit_button.grid(row=0, column=2, padx=5)

        self.export_button = tk.Button(self.action_frame, text="Export to CSV", font=("Arial", 12), command=self.export_posts)
        self.export_button.grid(row=0, column=3, padx=5)

        # Load posts from file if exists
        self.load_posts()

    def add_post(self):
        """Add a new post."""
        content = self.add_post_entry.get().strip()
        tags = self.add_tags_entry.get().strip().split(",") if self.add_tags_entry.get().strip() else []
        if content:
            post_id = self.post_counter
            self.posts[post_id] = {"content": content, "tags": tags}
            self.tags_history.update(tags)
            self.post_counter += 1
            messagebox.showinfo("Success", f"Post created with ID {post_id}!")
            self.add_post_entry.delete(0, tk.END)
            self.add_tags_entry.delete(0, tk.END)
            self.view_posts()  # Refresh posts
        else:
            messagebox.showwarning("Warning", "Post content cannot be empty!")

    def delete_post(self):
        """Delete the selected post."""
        selected_index = self.post_listbox.curselection()
        if selected_index:
            post_id = int(self.post_listbox.get(selected_index).split(":")[0].strip())
            if post_id in self.posts:
                del self.posts[post_id]
                messagebox.showinfo("Success", f"Post with ID {post_id} deleted!")
                self.view_posts()  # Refresh posts
        else:
            messagebox.showwarning("Warning", "Please select a post to delete!")

    def edit_post(self):
        """Edit the selected post."""
        selected_index = self.post_listbox.curselection()
        if selected_index:
            post_id = int(self.post_listbox.get(selected_index).split(":")[0].strip())
            post_data = self.posts[post_id]
            new_content = self.add_post_entry.get().strip()
            new_tags = self.add_tags_entry.get().strip().split(",") if self.add_tags_entry.get().strip() else []

            if new_content:
                self.posts[post_id] = {"content": new_content, "tags": new_tags}
                messagebox.showinfo("Success", f"Post with ID {post_id} updated!")
                self.view_posts()  # Refresh posts
            else:
                messagebox.showwarning("Warning", "Post content cannot be empty!")
        else:
            messagebox.showwarning("Warning", "Please select a post to edit!")

    def view_posts(self):
        """Refresh the post list."""
        self.post_listbox.delete(0, tk.END)
        for post_id, post_data in self.posts.items():
            self.post_listbox.insert(tk.END, f"{post_id}: {post_data['content']}")

    def show_post_details(self, event):
        """Show details of the selected post."""
        selected_index = self.post_listbox.curselection()
        if selected_index:
            post_id = int(self.post_listbox.get(selected_index).split(":")[0].strip())
            post_data = self.posts[post_id]
            tags = ", ".join(post_data["tags"]) if post_data["tags"] else "No tags assigned."
            messagebox.showinfo("Post Details", f"Post ID: {post_id}\nContent: {post_data['content']}\nTags: {tags}")

    def search_posts(self, event):
        """Search posts based on keywords in the content."""
        search_term = self.search_entry.get().lower()
        self.post_listbox.delete(0, tk.END)
        for post_id, post_data in self.posts.items():
            if search_term in post_data["content"].lower():
                self.post_listbox.insert(tk.END, f"{post_id}: {post_data['content']}")

    def export_posts(self):
        """Export all posts to a CSV file."""
        with open("posts.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Post ID", "Content", "Tags"])
            for post_id, post_data in self.posts.items():
                tags = ", ".join(post_data["tags"]) if post_data["tags"] else ""
                writer.writerow([post_id, post_data["content"], tags])
        messagebox.showinfo("Success", "Posts exported to posts.csv")

    def load_posts(self):
        """Load posts from a file if it exists."""
        if os.path.exists("posts.csv"):
            with open("posts.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    post_id = int(row[0])
                    content = row[1]
                    tags = row[2].split(",") if row[2] else []
                    self.posts[post_id] = {"content": content, "tags": tags}
                    self.post_counter = post_id + 1  # Update post counter


if __name__ == "__main__":
    root = tk.Tk()
    app = SocialMediaPostManagerGUI(root)
    root.mainloop()

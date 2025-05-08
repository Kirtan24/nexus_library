import customtkinter as ctk
from tkinter import messagebox

# Sample data
data = [
    {"ID": 1, "Name": "The Pragmatic Programmer", "Author": "Andy Hunt"},
    {"ID": 2, "Name": "Clean Code", "Author": "Robert C. Martin"},
    {"ID": 3, "Name": "Design Patterns", "Author": "Erich Gamma"},
]

class DataTable(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        # Header
        headers = ["ID", "Name", "Author", "Actions"]
        for col, text in enumerate(headers):
            label = ctk.CTkLabel(self, text=text, font=("Arial", 16, "bold"))
            label.grid(row=0, column=col, padx=10, pady=10)

        # Data rows
        for row_idx, book in enumerate(data, start=1):
            ctk.CTkLabel(self, text=book["ID"]).grid(row=row_idx, column=0, padx=10)
            ctk.CTkLabel(self, text=book["Name"]).grid(row=row_idx, column=1, padx=10)
            ctk.CTkLabel(self, text=book["Author"]).grid(row=row_idx, column=2, padx=10)

            # Actions
            view_btn = ctk.CTkButton(self, text="View", width=60, command=lambda b=book: self.view_item(b))
            edit_btn = ctk.CTkButton(self, text="Edit", width=60, command=lambda b=book: self.edit_item(b))
            delete_btn = ctk.CTkButton(self, text="Delete", width=60, fg_color="red", command=lambda b=book: self.delete_item(b))

            view_btn.grid(row=row_idx, column=3, padx=2, pady=5, sticky="w")
            edit_btn.grid(row=row_idx, column=3, padx=65, pady=5, sticky="w")
            delete_btn.grid(row=row_idx, column=3, padx=130, pady=5, sticky="w")

    def view_item(self, item):
        messagebox.showinfo("View Item", f"Viewing:\n{item}")

    def edit_item(self, item):
        messagebox.showinfo("Edit Item", f"Editing:\n{item}")

    def delete_item(self, item):
        confirm = messagebox.askyesno("Confirm Delete", f"Delete '{item['Name']}'?")
        if confirm:
            messagebox.showinfo("Deleted", f"{item['Name']} deleted!")
            # You'd also update the data model and refresh the UI here
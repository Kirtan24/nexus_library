import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from app.repositories.borrow_repository import BorrowRepository
from app.repositories.book_repository import BookRepository

class MyBorrowedBooksPage(ctk.CTkFrame):
    def __init__(self, master, user_id, back_callback=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.user_id = user_id
        self.back_callback = back_callback
        self.borrow_repo = BorrowRepository()
        self.book_repo = BookRepository()

        self.create_widgets()
        self.load_borrowed_books()

    def create_widgets(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=10)

        self.back_button = ctk.CTkButton(
            self.header_frame,
            text="←",
            command=self.go_back,
            fg_color="#6f23ff",
            hover_color="#5a1dcc",
            text_color="#ffffff",
            width=100,
            height=35,
            corner_radius=8
        )
        self.back_button.pack(side="left", padx=5)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="My Borrowed Books",
            font=("Arial", 20, "bold")
        )
        self.title_label.pack(side="left", padx=10)

        self.content_frame = ctk.CTkScrollableFrame(self)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.empty_label = ctk.CTkLabel(
            self.content_frame,
            text="You haven't borrowed any books yet",
            font=("Arial", 14)
        )

    def go_back(self):
        self.master.show_home_page()

    def load_borrowed_books(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        borrow_records = self.borrow_repo.get_user_borrow_history(self.user_id)
        active_borrows = [r for r in borrow_records if r['return_date'] is None]

        if not active_borrows:
            self.empty_label.pack(pady=50)
            return

        for i, record in enumerate(active_borrows):
            book = self.book_repo.get_item(record['item_id'])
            if not book:
                continue

            card = ctk.CTkFrame(self.content_frame)
            card.pack(fill="x", pady=5, padx=5)

            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=10)

            ctk.CTkLabel(
                info_frame,
                text=book['title'],
                font=("Arial", 14, "bold"),
                anchor="w"
            ).pack(fill="x")

            ctk.CTkLabel(
                info_frame,
                text=f"Author: {book.get('author_name', 'Unknown')}",
                anchor="w"
            ).pack(fill="x")

            ctk.CTkLabel(
                info_frame,
                text=f"Due Date: {record['due_date'].strftime('%Y-%m-%d')}",
                anchor="w"
            ).pack(fill="x")

            return_btn = ctk.CTkButton(
                card,
                text="Return Book",
                fg_color="#D35B58",
                command=lambda r=record: self.return_book(r['record_id'])
            )
            return_btn.pack(side="right", padx=10)

    def return_book(self, record_id):
        try:
            return_date = datetime.now().date()

            record = self.borrow_repo.get_borrow_record(record_id)
            if not record:
                messagebox.showerror("Error", "Borrow record not found")
                return

            fine_amount = 0.0
            if return_date > record['due_date']:
                days_overdue = (return_date - record['due_date']).days
                fine_amount = days_overdue * 5.0

            success, _ = self.borrow_repo.close_borrow_record(
                record_id,
                return_date,
                fine_amount
            )

            if success:
                book = self.book_repo.get_item(record['item_id'])
                if book and book['item_type'] == 'PrintedBook':
                    current_copies = book.get('available_copies', 0)
                    self.book_repo.update_item(
                        record['item_id'],
                        'PrintedBook',
                        available_copies=current_copies + 1,
                        availability_status='Available'
                    )

                messagebox.showinfo("Success", "Book returned successfully")
                self.load_borrowed_books()
            else:
                messagebox.showerror("Error", "Failed to return book")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book: {str(e)}")
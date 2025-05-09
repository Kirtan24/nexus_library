import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from app.controllers.db_controller import DatabaseController
from app.services.observer_service import ObserverService
from app.repositories.book_repository import BookRepository
from app.repositories.borrow_repository import BorrowRepository

class BookDetailView(ctk.CTkFrame):
    def __init__(self, master, item_id, user_id):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.item_id = item_id
        self.user_id = user_id
        self.book_repo = BookRepository()
        self.borrow_repo = BorrowRepository()
        self.observer_service = ObserverService()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_widgets()
        self.load_book_details()

    def create_widgets(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1)

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
        self.back_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="",
            font=("Arial", 20, "bold"),
            anchor="w"
        )
        self.title_label.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.details_frame = ctk.CTkScrollableFrame(self)
        self.details_frame.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")
        self.details_frame.grid_columnconfigure(1, weight=1)

        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="ew")
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)

        self.action_button = ctk.CTkButton(
            self.buttons_frame,
            text="",
            command=self.handle_action,
            height=40
        )
        self.action_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

    def go_back(self):
        """Return to the previous view using the callback"""
        self.master.show_browse_page()

    def load_book_details(self):
        book = self.book_repo.get_item(self.item_id)
        if not book:
            messagebox.showerror("Error", "Book details not found")
            self.go_back()
            return

        self.title_label.configure(text=book['title'])

        for widget in self.details_frame.winfo_children():
            widget.destroy()

        row = 0
        details = [
            ("Author", book.get('author_name', 'Unknown')),
            ("Genre", book.get('genre', 'Not specified')),
            ("Publication Year", book.get('publication_year', 'Unknown')),
            ("Status", book.get('availability_status', 'Unknown'))
        ]

        for label, value in details:
            ctk.CTkLabel(
                self.details_frame,
                text=f"{label}:",
                font=("Arial", 12, "bold"),
                anchor="e"
            ).grid(row=row, column=0, padx=5, pady=5, sticky="e")

            ctk.CTkLabel(
                self.details_frame,
                text=value,
                anchor="w"
            ).grid(row=row, column=1, padx=5, pady=5, sticky="w")
            row += 1

        if book['item_type'] == 'PrintedBook':
            self.display_printed_book_details(book, row)
        elif book['item_type'] == 'EBook':
            self.display_ebook_details(book, row)
        elif book['item_type'] == 'ResearchPaper':
            self.display_research_paper_details(book, row)
        elif book['item_type'] == 'AudioBook':
            self.display_audiobook_details(book, row)

        self.configure_action_button(book)

    def display_printed_book_details(self, book, start_row):
        details = [
            ("ISBN", book.get('isbn', 'Not available')),
            ("Shelf Location", book.get('shelf_location', 'Not specified')),
            ("Total Copies", book.get('total_copies', 1)),
            ("Available Copies", book.get('available_copies', 1))
        ]

        for i, (label, value) in enumerate(details):
            ctk.CTkLabel(
                self.details_frame,
                text=f"{label}:",
                font=("Arial", 12, "bold"),
                anchor="e"
            ).grid(row=start_row+i, column=0, padx=5, pady=5, sticky="e")

            ctk.CTkLabel(
                self.details_frame,
                text=value,
                anchor="w"
            ).grid(row=start_row+i, column=1, padx=5, pady=5, sticky="w")

    def display_ebook_details(self, book, start_row):
        details = [
            ("Description", book.get('description', 'No description available')),
        ]

        for i, (label, value) in enumerate(details):
            ctk.CTkLabel(
                self.details_frame,
                text=f"{label}:",
                font=("Arial", 12, "bold"),
                anchor="e"
            ).grid(row=start_row+i, column=0, padx=5, pady=5, sticky="e")

            # Use a textbox for longer descriptions
            if label == "Description":
                textbox = ctk.CTkTextbox(
                    self.details_frame,
                    width=400,
                    height=100,
                    wrap="word",
                    activate_scrollbars=True
                )
                textbox.insert("1.0", value)
                textbox.configure(state="disabled")
                textbox.grid(row=start_row+i, column=1, padx=5, pady=5, sticky="w")
            else:
                ctk.CTkLabel(
                    self.details_frame,
                    text=value,
                    anchor="w"
                ).grid(row=start_row+i, column=1, padx=5, pady=5, sticky="w")

    def display_research_paper_details(self, book, start_row):
        details = [
            ("Abstract", book.get('abstract', 'No abstract available')),
            ("Journal", book.get('journal_name', 'Not specified')),
            ("DOI", book.get('doi', 'Not available'))
        ]

        for i, (label, value) in enumerate(details):
            ctk.CTkLabel(
                self.details_frame,
                text=f"{label}:",
                font=("Arial", 12, "bold"),
                anchor="e"
            ).grid(row=start_row+i, column=0, padx=5, pady=5, sticky="e")

            if label == "Abstract":
                textbox = ctk.CTkTextbox(
                    self.details_frame,
                    width=400,
                    height=100,
                    wrap="word",
                    activate_scrollbars=True
                )
                textbox.insert("1.0", value)
                textbox.configure(state="disabled")
                textbox.grid(row=start_row+i, column=1, padx=5, pady=5, sticky="w")
            else:
                ctk.CTkLabel(
                    self.details_frame,
                    text=value,
                    anchor="w"
                ).grid(row=start_row+i, column=1, padx=5, pady=5, sticky="w")

    def display_audiobook_details(self, book, start_row):
        details = [
            ("Narrator", book.get('narrator', 'Unknown')),
            ("Duration", f"{book.get('duration_minutes', 0)} minutes"),
            ("Description", book.get('description', 'No description available'))
        ]

        for i, (label, value) in enumerate(details):
            ctk.CTkLabel(
                self.details_frame,
                text=f"{label}:",
                font=("Arial", 12, "bold"),
                anchor="e"
            ).grid(row=start_row+i, column=0, padx=5, pady=5, sticky="e")

            if label == "Description":
                textbox = ctk.CTkTextbox(
                    self.details_frame,
                    width=400,
                    height=100,
                    wrap="word",
                    activate_scrollbars=True
                )
                textbox.insert("1.0", value)
                textbox.configure(state="disabled")
                textbox.grid(row=start_row+i, column=1, padx=5, pady=5, sticky="w")
            else:
                ctk.CTkLabel(
                    self.details_frame,
                    text=value,
                    anchor="w"
                ).grid(row=start_row+i, column=1, padx=5, pady=5, sticky="w")

    def configure_action_button(self, book):
        if book['item_type'] == 'PrintedBook':
            # Check if user has an active borrow record for this book
            active_borrow = self.borrow_repo.get_active_borrow_record(self.user_id, self.item_id)

            if active_borrow:
                self.action_button.configure(
                    text="Return Book",
                    state="normal",
                    fg_color="#D35B58",  # Red color for return action
                    command=self.return_book
                )
            elif book.get('available_copies', 0) > 0:
                self.action_button.configure(
                    text="Borrow Book",
                    state="normal",
                    fg_color="#2E8B57",  # Green color for borrow
                    command=self.borrow_book
                )
            else:
                self.action_button.configure(
                    text="Notify When Available",
                    state="normal",
                    fg_color="#4682B4",  # Blue color for notify
                    command=self.register_for_notification
                )
        elif book['item_type'] == 'EBook':
            self.action_button.configure(
                text="Download EBook",
                state="normal",
                fg_color="#4169E1",  # Royal blue for download
                command=self.download_ebook
            )
        elif book['item_type'] == 'AudioBook':
            self.action_button.configure(
                text="Listen to Sample",
                state="normal",
                fg_color="#9370DB",  # Medium purple for audio
                command=self.play_audio_sample
            )
        else:
            self.action_button.configure(
                text="View Details",
                state="normal",
                fg_color="#708090",  # Slate gray for view
                command=self.view_details
            )

    def handle_action(self):
        book = self.book_repo.get_item(self.item_id)
        if not book:
            messagebox.showerror("Error", "Book details not found")
            return

        action = self.action_button.cget("text")

        if action == "Borrow Book":
            self.borrow_book()
        elif action == "Return Book":
            self.return_book()
        elif action == "Notify When Available":
            self.register_for_notification()
        elif action == "Download EBook":
            self.download_ebook()
        elif action == "Listen to Sample":
            self.play_audio_sample()

    def borrow_book(self):
        try:
            existing_borrow = self.borrow_repo.get_active_borrow_record(self.user_id, self.item_id)
            if existing_borrow:
                messagebox.showwarning(
                    "Already Borrowed",
                    "You already have this book checked out. Please return it before borrowing again."
                )
                return

            borrow_date = datetime.now().date()
            due_date = borrow_date + timedelta(days=14)

            success, result = self.borrow_repo.create_borrow_record(
                self.user_id,
                self.item_id,
                borrow_date,
                due_date
            )

            if success:
                current_copies = self.book_repo.get_item(self.item_id).get('available_copies', 1)
                self.book_repo.update_item(
                    self.item_id,
                    'PrintedBook',
                    available_copies=current_copies - 1
                )

                if current_copies - 1 == 0:
                    self.book_repo.update_item(
                        self.item_id,
                        'PrintedBook',
                        availability_status='Unavailable'
                    )

                messagebox.showinfo("Success", f"Book borrowed successfully. Due date: {due_date}")
                self.load_book_details()
            else:
                messagebox.showerror("Error", result)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to borrow book: {str(e)}")

    # def return_book(self):
    #     try:
    #         # Get the active borrow record
    #         borrow_record = self.borrow_repo.get_active_borrow_record(self.user_id, self.item_id)
    #         if not borrow_record:
    #             messagebox.showerror("Error", "No active borrow record found")
    #             return

    #         # Calculate fine if overdue
    #         return_date = datetime.now().date()
    #         due_date = borrow_record['due_date']
    #         fine_amount = 0.0

    #         if return_date > due_date:
    #             days_overdue = (return_date - due_date).days
    #             fine_amount = days_overdue * 5.0
    #             messagebox.showwarning(
    #                 "Overdue Book",
    #                 f"This book is {days_overdue} days overdue. A fine of ${fine_amount:.2f} will be charged."
    #             )

    #         success, result = self.borrow_repo.close_borrow_record(
    #             borrow_record['record_id'],
    #             return_date,
    #             fine_amount
    #         )

    #         if success:
    #             current_copies = self.book_repo.get_item(self.item_id).get('available_copies', 0)
    #             self.book_repo.update_item(
    #                 self.item_id,
    #                 'PrintedBook',
    #                 available_copies=current_copies + 1,
    #                 availability_status='Available' if current_copies + 1 > 0 else 'Checked Out'
    #             )

    #             if fine_amount > 0:
    #                 self.borrow_repo.create_fine(
    #                     self.user_id,
    #                     borrow_record['record_id'],
    #                     fine_amount
    #                 )

    #             messagebox.showinfo("Success", "Book returned successfully")
    #             self.load_book_details()  # Refresh the view


    #         else:
    #             messagebox.showerror("Error", result)
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Failed to return book: {str(e)}")

    def return_book(self):
        try:
            borrow_record = self.borrow_repo.get_active_borrow_record(self.user_id, self.item_id)
            if not borrow_record:
                messagebox.showerror("Error", "No active borrow record found")
                return

            return_date = datetime.now().date()
            due_date = borrow_record['due_date']
            fine_amount = 0.0

            if return_date > due_date:
                days_overdue = (return_date - due_date).days
                fine_amount = days_overdue * 5.0
                messagebox.showwarning(
                    "Overdue Book",
                    f"This book is {days_overdue} days overdue. A fine of ${fine_amount:.2f} will be charged."
                )

            success, result = self.borrow_repo.close_borrow_record(
                borrow_record['record_id'],
                return_date,
                fine_amount
            )

            if not success:
                messagebox.showerror("Error", result)
                return

            book_details = self.book_repo.get_item(self.item_id)
            if not book_details:
                messagebox.showerror("Error", "Book details not found")
                return

            if book_details['item_type'] == 'PrintedBook':
                current_copies = book_details.get('available_copies', 0)
                total_copies = book_details.get('total_copies', 1)
                new_copies = current_copies + 1

                if new_copies > total_copies:
                    messagebox.showerror("Error", "Cannot return more copies than total inventory")
                    return

                new_status = 'Available' if new_copies > 0 else 'Unavailable'

                success, message = self.book_repo.update_item(
                    self.item_id,
                    'PrintedBook',
                    available_copies=new_copies,
                    availability_status=new_status
                )

                if new_status == 'Available' and current_copies == 0:
                    self.observer_service.notify(self.item_id)
            else:
                success, message = self.book_repo.update_item(
                    self.item_id,
                    book_details['item_type'],
                    availability_status='Available'
                )

                self.observer_service.notify(self.item_id)

            if not success:
                messagebox.showerror("Error", message)
                return

            if fine_amount > 0:
                fine_success, fine_result = self.borrow_repo.create_fine(
                    self.user_id,
                    borrow_record['record_id'],
                    fine_amount
                )
                if not fine_success:
                    messagebox.showwarning("Warning", f"Book returned but failed to create fine: {fine_result}")

            messagebox.showinfo("Success", "Book returned successfully")
            self.load_book_details()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book: {str(e)}")

    def register_for_notification(self):
        try:
            db = DatabaseController()
            query = """
                SELECT observer_id FROM item_observers
                WHERE user_id = %s AND item_id = %s AND status = 'active'
            """
            existing = db.execute_query(query, (self.user_id, self.item_id), True)

            if existing:
                messagebox.showinfo("Info", "You're already registered for notifications on this item")
                return

            observer_id = self.observer_service.add(self.user_id, self.item_id)
            if observer_id:
                messagebox.showinfo("Success", "You'll be notified when this item becomes available")
            else:
                messagebox.showerror("Error", "Failed to register for notifications")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register for notifications: {str(e)}")

    def download_ebook(self):
        messagebox.showinfo("Download", "EBook download will start shortly")

    def play_audio_sample(self):
        messagebox.showinfo("Audio Sample", "Playing audio sample...")

    def view_details(self):
        messagebox.showinfo("Research Paper", "Research paper details...")

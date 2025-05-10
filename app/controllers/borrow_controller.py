from app.repositories.borrow_repository import BorrowRepository
from app.repositories.book_repository import BookRepository
from app.repositories.user_repository import UserRepository
from app.services.borrow_decorator import FacultyBorrowDecorator
from datetime import datetime, timedelta

class BorrowController:
    def __init__(self, user_repository=None):
        self.borrow_repository = BorrowRepository()
        self.book_repository = BookRepository()
        self.user_repository = UserRepository()

    def get_controller_for_user(self, user_id):
        """Get appropriate controller based on user type"""
        if not self.user_repository:
            return self

        user = self.user_repository.get_user_by_id(user_id)
        if user and user.get('user_type') == 'faculty':
            return FacultyBorrowDecorator(self)
        return self

    def create_borrow_record(self, user_id, book_id):
        book_result = self.book_repository.get_item(book_id)
        if not book_result:
            return False, ["Book not found"]

        if book_result.get('availability_status') != 'available':
            return False, ["Book is not available for borrowing"]

        existing_borrow = self.borrow_repository.get_active_borrow_record(user_id, book_id)
        if existing_borrow:
            return False, ["User already has this book checked out"]

        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=14)

        success, result = self.borrow_repository.create_borrow_record(
            user_id, book_id, borrow_date, due_date
        )

        if not success:
            return False, [result]

        status_update, status_message = self.book_repository.update_book_status(book_id, "borrowed")
        if not status_update:
            print(f"Failed to update book status after borrowing: {status_message}")

        return True, f"Book borrowed successfully. Due date: {due_date.strftime('%Y-%m-%d')}"

    def update_book_availability(self, book_id, status):
        """Update the availability status of a book"""
        return self.book_repository.update_book_status(book_id, status)

    def get_active_borrow_record(self, user_id, book_id):
        return self.borrow_repository.get_active_borrow_record(user_id, book_id)

    def return_book(self, user_id, book_id):
        borrow_record = self.borrow_repository.get_active_borrow_record(user_id, book_id)
        if not borrow_record:
            return False, ["No active borrow record found for this user and book"]

        return_date = datetime.now()
        fine_amount = 0.0

        if return_date.date() > borrow_record['due_date'].date():
            overdue_days = (return_date.date() - borrow_record['due_date'].date()).days
            fine_amount = overdue_days * 5

        success, message = self.borrow_repository.close_borrow_record(
            borrow_record['record_id'], return_date, fine_amount
        )

        if not success:
            return False, [message]

        self.borrow_repository.update_book_availability(book_id, borrowed=False)

        if fine_amount > 0:
            return True, f"Book returned successfully. Fine for overdue: ${fine_amount:.2f}"
        return True, "Book returned successfully"

    def calculate_fine(self, record_id):
        borrow_record = self.get_borrow_record(record_id)

        if not borrow_record:
            return False, ["Borrow record not found"]

        if borrow_record.return_date is None and datetime.now() > borrow_record.due_date:
            overdue_days = (datetime.now().date() - borrow_record.due_date.date()).days
            fine_amount = overdue_days * 5

            self.borrow_repository.update_fine_amount(record_id, fine_amount)

            return True, fine_amount
        elif borrow_record.return_date is not None and borrow_record.return_date > borrow_record.due_date:
            return True, borrow_record.fine_amount

        return True, 0.0

    def get_user_fines(self, user_id):
        return self.borrow_repository.get_user_fines(user_id)

    def get_overdue_records(self):
        current_date = datetime.now()
        return self.borrow_repository.get_overdue_borrow_records(current_date)

    def get_user_borrow_history(self, user_id):
        return self.borrow_repository.get_user_borrow_history(user_id)

    def extend_due_date(self, record_id, days=7):
        borrow_record = self.get_borrow_record(record_id)

        if not borrow_record:
            return False, ["Borrow record not found"]

        if borrow_record.return_date is not None:
            return False, ["Cannot extend due date for already returned book"]

        new_due_date = borrow_record.due_date + timedelta(days=days)

        query = """
            UPDATE borrow_records
            SET due_date = %s
            WHERE record_id = %s
            RETURNING record_id;
        """

        result = self.borrow_repository.db_controller.execute_query(
            query, (new_due_date, record_id), True
        )

        if not result:
            return False, ["Failed to extend due date"]

        return True, f"Due date extended to {new_due_date.strftime('%Y-%m-%d')}"
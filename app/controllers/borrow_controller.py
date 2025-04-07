from app.models import BorrowRecord
from repositories.borrow_repository import BorrowRepository
from repositories.book_repository import BookRepository
from datetime import datetime, timedelta
import logging

class BorrowController:
    def __init__(self):
        self.borrow_repository = BorrowRepository()
        self.book_repository = BookRepository()
        logging.info("Borrow controller initialized")

    def create_borrow_record(self, user_id, book_id):
        book_result = self.book_repository.get_book(book_id)
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
            logging.error(f"Failed to update book status after borrowing: {status_message}")

        logging.info(f"User {user_id} borrowed book {book_id}. Due: {due_date}")
        return True, f"Book borrowed successfully. Due date: {due_date.strftime('%Y-%m-%d')}"

    def get_borrow_record(self, record_id):
        result = self.borrow_repository.get_borrow_record(record_id)

        if not result:
            return None

        borrow_record = BorrowRecord(
            record_id=result['record_id'],
            user_id=result['user_id'],
            book_id=result['book_id'],
            borrow_date=result['borrow_date'],
            due_date=result['due_date'],
            return_date=result['return_date'],
            fine_amount=result['fine_amount']
        )

        return borrow_record

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

        status_update, status_message = self.book_repository.update_book_status(book_id, "available")
        if not status_update:
            logging.error(f"Failed to update book status after return: {status_message}")

        if fine_amount > 0:
            return True, f"Book returned successfully. Fine for overdue: ${fine_amount:.2f}"
        else:
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

        logging.info(f"Due date extended for record {record_id} to {new_due_date}")
        return True, f"Due date extended to {new_due_date.strftime('%Y-%m-%d')}"
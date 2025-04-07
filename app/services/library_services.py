from controllers.book_controller import BookController
from controllers.borrow_controller import BorrowController
from controllers.reservation_controller import ReservationController

import logging

class LibraryService:
    """
    Service class to handle library operations like borrowing, returning,
    reserving books, and managing late fees.
    Implements Facade pattern for simplified interactions.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LibraryService, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return

        self.book_controller = BookController()
        self.borrow_controller = BorrowController()
        self.reservation_controller = ReservationController()
        self.initialized = True
        logging.info("Library Service initialized")

    def borrow_book(self, user_id, book_id):
        """Handles borrowing a book"""
        book = self.book_controller.get_book(book_id)
        if not book:
            return False, "Book not found"

        if book.availability_status != "Available":
            return False, "Book is not available for borrowing"

        success, message = self.borrow_controller.create_borrow_record(user_id, book_id)
        if success:
            self.book_controller.update_book_status(book_id, "Borrowed")
        return success, message

    def return_book(self, user_id, book_id):
        """Handles returning a book"""
        borrow_record = self.borrow_controller.get_active_borrow_record(user_id, book_id)
        if not borrow_record:
            return False, "No active borrow record found"

        fine_amount = self.borrow_controller.calculate_fine(borrow_record)
        self.borrow_controller.close_borrow_record(borrow_record.borrow_id)

        if fine_amount > 0:
            return False, f"Book returned, but there is a pending fine of ${fine_amount}"

        self.book_controller.update_book_status(book_id, "Available")
        return True, "Book returned successfully"

    def reserve_book(self, user_id, book_id):
        """Handles reserving a book"""
        book = self.book_controller.get_book(book_id)
        if not book:
            return False, "Book not found"

        if book.availability_status != "Borrowed":
            return False, "Book is available. No need for reservation."

        success, message = self.reservation_controller.create_reservation(user_id, book_id)
        return success, message

    def check_fine(self, user_id):
        """Check pending fines for a user"""
        return self.borrow_controller.get_user_fines(user_id)

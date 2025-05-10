from abc import ABC, abstractmethod
from datetime import timedelta

class BorrowDecorator(ABC):
    def __init__(self, borrow_controller):
        self._borrow_controller = borrow_controller

    @abstractmethod
    def create_borrow_record(self, user_id, book_id):
        pass

class FacultyBorrowDecorator(BorrowDecorator):
    def create_borrow_record(self, user_id, book_id):
        success, result = self._borrow_controller.create_borrow_record(user_id, book_id)

        if success:
            borrow_record = self._borrow_controller.get_active_borrow_record(user_id, book_id)
            if borrow_record:
                new_due_date = borrow_record['due_date'] + timedelta(days=14)
                self._borrow_controller.borrow_repository.extend_due_date(
                    borrow_record['record_id'],
                    (new_due_date - borrow_record['due_date']).days
                )
                return True, f"Book borrowed successfully. Due date: {new_due_date.strftime('%Y-%m-%d')} (Faculty Extended)"
        return success, result
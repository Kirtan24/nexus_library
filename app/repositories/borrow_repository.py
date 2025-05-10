from app.controllers.db_controller import DatabaseController
from app.services.observer_service import ObserverService

class BorrowRepository:
    def __init__(self):
        self.db_controller = DatabaseController()
        self.observer_service = ObserverService()

    def create_borrow_record(self, user_id, book_id, borrow_date, due_date):
        try:
            check_query = """
                SELECT record_id FROM borrow_records
                WHERE user_id = %s AND item_id = %s AND return_date IS NULL
            """
            existing_record = self.db_controller.execute_query(
                check_query,
                (user_id, book_id),
                True
            )

            if existing_record:
                return False, "You already have an active borrow record for this book"

            insert_query = """
                INSERT INTO borrow_records (user_id, item_id, borrow_date, due_date, return_date, fine_amount)
                VALUES (%s, %s, %s, %s, NULL, 0.0)
                RETURNING record_id;
            """
            result = self.db_controller.execute_query(
                insert_query,
                (user_id, book_id, borrow_date, due_date),
                True
            )

            if not result:
                return False, "Failed to create borrow record"

            record_id = result[0]['record_id']
            return True, record_id

        except Exception as e:
            return False, str(e)

    def update_book_availability(self, book_id, borrowed):
        try:
            status = "borrowed" if borrowed else "available"
            status_query = "UPDATE items SET availability_status = %s WHERE item_id = %s"
            self.db_controller.execute_query(status_query, (status, book_id))

            if not borrowed:
                self.observer_service.notify(book_id)

            return True
        except Exception as e:
            print(f"Error updating book availability: {e}")
            return False

    def get_borrow_record(self, record_id):
        try:
            query = """
                SELECT br.*, b.title as book_title, u.name as user_name
                FROM borrow_records br
                JOIN items b ON br.item_id = b.item_id
                JOIN users u ON br.user_id = u.user_id
                WHERE br.record_id = %s;
            """
            result = self.db_controller.execute_query(query, (record_id,), True)

            if not result:
                return None

            return result[0]

        except Exception as e:
            return None

    def get_active_borrow_record(self, user_id, book_id):
        """Check if user already has an active borrow record for this book"""
        try:
            query = """
                SELECT * FROM borrow_records
                WHERE user_id = %s AND item_id = %s AND return_date IS NULL
            """
            result = self.db_controller.execute_query(query, (user_id, book_id), True)
            return result[0] if result else None
        except Exception as e:
            print(f"Error checking active borrow record: {e}")
            return None

    def close_borrow_record(self, record_id, return_date, fine_amount=0.0):
        """Close a borrow record by setting return date and fine amount"""
        try:
            query = """
                UPDATE borrow_records
                SET return_date = %s, fine_amount = %s
                WHERE record_id = %s
                RETURNING record_id;
            """
            result = self.db_controller.execute_query(
                query,
                (return_date, fine_amount, record_id),
                True
            )
            return (True, "Borrow record closed") if result else (False, "Borrow record not found")
        except Exception as e:
            return False, str(e)

    def create_fine(self, user_id, borrow_record_id, amount):
        """Create a fine record for an overdue book"""
        try:
            query = """
                INSERT INTO fines (user_id, borrow_record_id, amount, status)
                VALUES (%s, %s, %s, 'unpaid')
                RETURNING fine_id;
            """
            result = self.db_controller.execute_query(
                query,
                (user_id, borrow_record_id, amount),
                True
            )
            return (True, result[0]['fine_id']) if result else (False, "Failed to create fine")
        except Exception as e:
            return False, str(e)

    def update_fine_amount(self, record_id, fine_amount):
        try:
            query = """
                UPDATE borrow_records
                SET fine_amount = %s
                WHERE record_id = %s
                RETURNING record_id;
            """
            result = self.db_controller.execute_query(query, (fine_amount, record_id), True)

            if not result:
                return False, "Borrow record not found"

            return True, "Fine amount updated successfully"

        except Exception as e:
            return False, str(e)

    def get_overdue_borrow_records(self, current_date):
        try:
            query = """
                SELECT br.*, b.title as book_title, u.name as user_name
                FROM borrow_records br
                JOIN books b ON br.book_id = b.book_id
                JOIN users u ON br.user_id = u.user_id
                WHERE br.return_date IS NULL AND br.due_date < %s
                ORDER BY br.due_date ASC;
            """
            results = self.db_controller.execute_query(query, (current_date,), True)
            return results

        except Exception as e:
            return []

    def get_user_borrow_history(self, user_id):
        try:
            query = """
                SELECT br.*, b.title as book_title
                FROM borrow_records br
                JOIN items b ON br.item_id = b.item_id
                WHERE br.user_id = %s
                ORDER BY br.borrow_date DESC;
            """
            results = self.db_controller.execute_query(query, (user_id,), True)
            return results

        except Exception as e:
            return []

    def get_book_borrow_history(self, book_id):
        try:
            query = """
                SELECT br.*, u.name as user_name
                FROM borrow_records br
                JOIN users u ON br.user_id = u.user_id
                WHERE br.book_id = %s
                ORDER BY br.borrow_date DESC;
            """
            results = self.db_controller.execute_query(query, (book_id,), True)
            return results

        except Exception as e:
            return []

    def get_user_fines(self, user_id):
        try:
            query = """
                SELECT SUM(fine_amount) as total_fine
                FROM borrow_records
                WHERE user_id = %s;
            """
            result = self.db_controller.execute_query(query, (user_id,), True)

            if not result or result[0]['total_fine'] is None:
                return 0.0

            return float(result[0]['total_fine'])

        except Exception as e:
            return 0.0
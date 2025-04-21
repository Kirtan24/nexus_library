from controllers.db_controller import DatabaseController
import logging

class BorrowRepository:
    def __init__(self):
        self.db_controller = DatabaseController()
        logging.info("BorrowRepository initialized")

    def create_borrow_record(self, user_id, book_id, borrow_date, due_date):
        try:
            query = """
                INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date, return_date, fine_amount)
                VALUES (%s, %s, %s, %s, NULL, 0.0)
                RETURNING record_id;
            """
            result = self.db_controller.execute_query(
                query,
                (user_id, book_id, borrow_date, due_date),
                True
            )

            if not result:
                return False, "Failed to create borrow record"

            record_id = result[0]['record_id']
            logging.info(f"Borrow record created for user {user_id}, book {book_id}, ID {record_id}")
            return True, record_id

        except Exception as e:
            logging.error(f"Failed to create borrow record: {e}")
            return False, str(e)

    def get_borrow_record(self, record_id):
        try:
            query = """
                SELECT br.*, b.title as book_title, u.name as user_name
                FROM borrow_records br
                JOIN books b ON br.book_id = b.book_id
                JOIN users u ON br.user_id = u.user_id
                WHERE br.record_id = %s;
            """
            result = self.db_controller.execute_query(query, (record_id,), True)

            if not result:
                return None

            return result[0]

        except Exception as e:
            logging.error(f"Failed to retrieve borrow record: {e}")
            return None

    def get_active_borrow_record(self, user_id, book_id):
        try:
            query = """
                SELECT *
                FROM borrow_records
                WHERE user_id = %s AND book_id = %s AND return_date IS NULL;
            """
            result = self.db_controller.execute_query(query, (user_id, book_id), True)

            if not result:
                return None

            return result[0]

        except Exception as e:
            logging.error(f"Failed to retrieve active borrow record: {e}")
            return None

    def close_borrow_record(self, record_id, return_date, fine_amount=0.0):
        try:
            query = """
                UPDATE borrow_records
                SET return_date = %s, fine_amount = %s
                WHERE record_id = %s
                RETURNING record_id;
            """
            result = self.db_controller.execute_query(query, (return_date, fine_amount, record_id), True)

            if not result:
                return False, "Borrow record not found"

            logging.info(f"Borrow record {record_id} closed with return date {return_date}")
            return True, "Borrow record closed successfully"

        except Exception as e:
            logging.error(f"Failed to close borrow record: {e}")
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

            logging.info(f"Borrow record {record_id} fine updated to {fine_amount}")
            return True, "Fine amount updated successfully"

        except Exception as e:
            logging.error(f"Failed to update fine amount: {e}")
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
            logging.error(f"Failed to retrieve overdue records: {e}")
            return []

    def get_user_borrow_history(self, user_id):
        try:
            query = """
                SELECT br.*, b.title as book_title
                FROM borrow_records br
                JOIN books b ON br.book_id = b.book_id
                WHERE br.user_id = %s
                ORDER BY br.borrow_date DESC;
            """
            results = self.db_controller.execute_query(query, (user_id,), True)
            return results

        except Exception as e:
            logging.error(f"Failed to retrieve user borrow history: {e}")
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
            logging.error(f"Failed to retrieve book borrow history: {e}")
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
            logging.error(f"Failed to calculate user fines: {e}")
            return 0.0
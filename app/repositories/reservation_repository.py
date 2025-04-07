from app.models import Reservation
from controllers.db_controller import DatabaseController
import logging
from datetime import datetime

class ReservationRepository:
    def __init__(self):
        self.db_controller = DatabaseController()
        logging.info("ReservationRepository initialized")

    def create_reservation(self, user_id, book_id):
        try:
            query = """
                INSERT INTO reservations (user_id, book_id, reservation_date, status)
                VALUES (%s, %s, %s, %s) RETURNING reservation_id;
            """
            result = self.db_controller.execute_query(
                query,
                (user_id, book_id, datetime.now(), "Pending"),
                True
            )

            if not result:
                return False, "Failed to create reservation"

            reservation_id = result[0]['reservation_id']
            logging.info(f"Reservation created for user {user_id}, book {book_id}")
            return True, reservation_id

        except Exception as e:
            logging.error(f"Reservation creation failed: {e}")
            return False, str(e)

    def get_user_reservations(self, user_id):
        try:
            query = """
                SELECT r.reservation_id, r.user_id, r.book_id, r.reservation_date, r.status,
                       b.title as book_title, a.name as author_name
                FROM reservations r
                JOIN books b ON r.book_id = b.book_id
                LEFT JOIN authors a ON b.author_id = a.author_id
                WHERE r.user_id = %s
                ORDER BY r.reservation_date DESC;
            """
            results = self.db_controller.execute_query(query, (user_id,), True)
            return results

        except Exception as e:
            logging.error(f"Failed to retrieve user reservations: {e}")
            return []

    def get_book_reservations(self, book_id):
        try:
            query = """
                SELECT r.reservation_id, r.user_id, r.book_id, r.reservation_date, r.status,
                       u.name as user_name
                FROM reservations r
                JOIN users u ON r.user_id = u.user_id
                WHERE r.book_id = %s
                ORDER BY r.reservation_date ASC;
            """
            results = self.db_controller.execute_query(query, (book_id,), True)
            return results

        except Exception as e:
            logging.error(f"Failed to retrieve book reservations: {e}")
            return []

    def update_reservation_status(self, reservation_id, status):
        try:
            query = """
                UPDATE reservations
                SET status = %s
                WHERE reservation_id = %s
                RETURNING reservation_id;
            """
            result = self.db_controller.execute_query(query, (status, reservation_id), True)

            if not result:
                return False, "Reservation not found"

            logging.info(f"Reservation {reservation_id} status updated to {status}")
            return True, "Reservation status updated successfully"

        except Exception as e:
            logging.error(f"Failed to update reservation status: {e}")
            return False, str(e)

    def cancel_reservation(self, reservation_id):
        return self.update_reservation_status(reservation_id, "Cancelled")

    def complete_reservation(self, reservation_id):
        return self.update_reservation_status(reservation_id, "Completed")

    def get_reservation_by_id(self, reservation_id):
        try:
            query = """
                SELECT r.reservation_id, r.user_id, r.book_id, r.reservation_date, r.status,
                       b.title as book_title, a.name as author_name
                FROM reservations r
                JOIN books b ON r.book_id = b.book_id
                LEFT JOIN authors a ON b.author_id = a.author_id
                WHERE r.reservation_id = %s;
            """
            result = self.db_controller.execute_query(query, (reservation_id,), True)

            if not result:
                return None

            return result[0]

        except Exception as e:
            logging.error(f"Failed to retrieve reservation: {e}")
            return None

    def delete_reservation(self, reservation_id):
        try:
            query = "DELETE FROM reservations WHERE reservation_id = %s RETURNING reservation_id;"
            result = self.db_controller.execute_query(query, (reservation_id,), True)

            if not result:
                return False, "Reservation not found"

            logging.info(f"Reservation {reservation_id} deleted")
            return True, "Reservation deleted successfully"

        except Exception as e:
            logging.error(f"Failed to delete reservation: {e}")
            return False, str(e)
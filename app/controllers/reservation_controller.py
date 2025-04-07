from ..models import Reservation
from ..repositories.reservation_repository import ReservationRepository
import logging

class ReservationController:
    def __init__(self):
        self.reservation_repository = ReservationRepository()
        logging.info("Reservation controller initialized")

    def create_reservation(self, user_id, book_id):
        success, result = self.reservation_repository.create_reservation(user_id, book_id)

        if success:
            reservation_id = result
            logging.info(f"User {user_id} reserved book {book_id}. Reservation ID: {reservation_id}")
            return True, "Book reserved successfully"
        else:
            logging.error(f"Reservation creation failed: {result}")
            return False, result

    def get_user_reservations(self, user_id):
        try:
            results = self.reservation_repository.get_user_reservations(user_id)

            reservations = []
            for row in results:
                reservation = Reservation(
                    reservation_id=row['reservation_id'],
                    user_id=row['user_id'],
                    book_id=row['book_id'],
                    reservation_date=row['reservation_date'],
                    status=row['status']
                )
                # Add additional information
                reservation.book_title = row['book_title']
                reservation.author_name = row.get('author_name')
                reservations.append(reservation)

            return reservations

        except Exception as e:
            logging.error(f"Failed to retrieve reservations: {e}")
            return []

    def get_book_reservations(self, book_id):
        results = self.reservation_repository.get_book_reservations(book_id)

        reservations = []
        for row in results:
            reservation = Reservation(
                reservation_id=row['reservation_id'],
                user_id=row['user_id'],
                book_id=row['book_id'],
                reservation_date=row['reservation_date'],
                status=row['status']
            )
            reservation.user_name = row['user_name']
            reservations.append(reservation)

        return reservations

    def update_reservation_status(self, reservation_id, status):
        valid_statuses = ["Pending", "Completed", "Cancelled"]
        if status not in valid_statuses:
            return False, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"

        success, message = self.reservation_repository.update_reservation_status(reservation_id, status)

        if success:
            logging.info(f"Reservation {reservation_id} status updated to {status}")
            return True, f"Reservation status updated to {status}"
        else:
            logging.error(f"Failed to update reservation status: {message}")
            return False, message

    def cancel_reservation(self, reservation_id):
        success, message = self.reservation_repository.cancel_reservation(reservation_id)

        if success:
            logging.info(f"Reservation {reservation_id} cancelled")
            return True, "Reservation cancelled successfully"
        else:
            logging.error(f"Failed to cancel reservation: {message}")
            return False, message

    def get_reservation_by_id(self, reservation_id):
        result = self.reservation_repository.get_reservation_by_id(reservation_id)

        if not result:
            return None

        reservation = Reservation(
            reservation_id=result['reservation_id'],
            user_id=result['user_id'],
            book_id=result['book_id'],
            reservation_date=result['reservation_date'],
            status=result['status']
        )
        reservation.book_title = result['book_title']
        reservation.author_name = result.get('author_name')

        return reservation
from app.models import Book
from controllers.db_controller import DatabaseController
import logging

class BookRepository:
    def __init__(self):
        self.db_controller = DatabaseController()
        logging.info("BookRepository initialized")

    def add_book(self, title, author_id, genre=None, publication_year=None, format=None, availability_status="available"):
        try:
            query = """
                INSERT INTO books (title, author_id, genre, publication_year, format, availability_status)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING book_id;
            """
            result = self.db_controller.execute_query(
                query,
                (title, author_id, genre, publication_year, format, availability_status),
                True
            )

            if not result:
                return False, "Failed to add book"

            book_id = result[0]['book_id']
            logging.info(f"Book '{title}' added with ID {book_id}")
            return True, book_id

        except Exception as e:
            logging.error(f"Failed to add book: {e}")
            return False, str(e)

    def get_book(self, book_id):
        try:
            query = """
                SELECT b.*, a.name as author_name
                FROM books b
                LEFT JOIN authors a ON b.author_id = a.author_id
                WHERE b.book_id = %s;
            """
            result = self.db_controller.execute_query(query, (book_id,), True)

            if not result:
                return None

            return result[0]

        except Exception as e:
            logging.error(f"Failed to retrieve book: {e}")
            return None

    def update_book(self, book_id, title=None, author_id=None, genre=None,
                    publication_year=None, format=None, availability_status=None):
        try:
            update_parts = []
            params = []

            if title is not None:
                update_parts.append("title = %s")
                params.append(title)

            if author_id is not None:
                update_parts.append("author_id = %s")
                params.append(author_id)

            if genre is not None:
                update_parts.append("genre = %s")
                params.append(genre)

            if publication_year is not None:
                update_parts.append("publication_year = %s")
                params.append(publication_year)

            if format is not None:
                update_parts.append("format = %s")
                params.append(format)

            if availability_status is not None:
                update_parts.append("availability_status = %s")
                params.append(availability_status)

            if not update_parts:
                return True, "No updates provided"

            query = f"""
                UPDATE books
                SET {', '.join(update_parts)}
                WHERE book_id = %s
                RETURNING book_id;
            """
            params.append(book_id)

            result = self.db_controller.execute_query(query, tuple(params), True)

            if not result:
                return False, "Book not found"

            logging.info(f"Book {book_id} updated")
            return True, "Book updated successfully"

        except Exception as e:
            logging.error(f"Failed to update book: {e}")
            return False, str(e)

    def delete_book(self, book_id):
        try:
            check_query = """
                SELECT COUNT(*) as count
                FROM borrow_records
                WHERE book_id = %s AND return_date IS NULL;
            """
            check_result = self.db_controller.execute_query(check_query, (book_id,), True)

            if check_result[0]['count'] > 0:
                return False, "Cannot delete book with active borrow records"

            delete_query = "DELETE FROM books WHERE book_id = %s RETURNING book_id;"
            result = self.db_controller.execute_query(delete_query, (book_id,), True)

            if not result:
                return False, "Book not found"

            logging.info(f"Book {book_id} deleted")
            return True, "Book deleted successfully"

        except Exception as e:
            logging.error(f"Failed to delete book: {e}")
            return False, str(e)

    def search_books(self, title=None, author=None, genre=None):
        try:
            query_parts = ["SELECT b.*, a.name as author_name FROM books b LEFT JOIN authors a ON b.author_id = a.author_id WHERE 1=1"]
            params = []

            if title:
                query_parts.append("AND b.title ILIKE %s")
                params.append(f"%{title}%")

            if author:
                query_parts.append("AND a.name ILIKE %s")
                params.append(f"%{author}%")

            if genre:
                query_parts.append("AND b.genre ILIKE %s")
                params.append(f"%{genre}%")

            query_parts.append("ORDER BY b.title ASC")
            query = " ".join(query_parts)

            results = self.db_controller.execute_query(query, tuple(params), True)
            return results

        except Exception as e:
            logging.error(f"Book search failed: {e}")
            return []

    def update_book_status(self, book_id, status):
        try:
            query = """
                UPDATE books
                SET availability_status = %s
                WHERE book_id = %s
                RETURNING book_id;
            """
            result = self.db_controller.execute_query(query, (status, book_id), True)

            if not result:
                return False, "Book not found"

            logging.info(f"Book {book_id} status updated to {status}")
            return True, "Book status updated successfully"

        except Exception as e:
            logging.error(f"Failed to update book status: {e}")
            return False, str(e)

    def get_available_books(self):
        try:
            query = """
                SELECT b.*, a.name as author_name
                FROM books b
                LEFT JOIN authors a ON b.author_id = a.author_id
                WHERE b.availability_status = 'available'
                ORDER BY b.title ASC;
            """
            results = self.db_controller.execute_query(query, None, True)
            return results

        except Exception as e:
            logging.error(f"Failed to retrieve available books: {e}")
            return []
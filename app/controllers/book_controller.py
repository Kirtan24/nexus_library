from app.models import Book
from repositories.book_repository import BookRepository
import logging
import re

class BookController:
    def __init__(self):
        self.book_repository = BookRepository()
        logging.info("Book controller initialized")

    def validate_book_data(self, title, author_id=None, genre=None, publication_year=None, format=None):
        errors = []

        if not title or len(title) < 2 or len(title) > 200:
            errors.append("Book title must be between 2 and 200 characters")

        if publication_year:
            try:
                year = int(publication_year)
                if year < 1000 or year > 9999:
                    errors.append("Publication year must be a valid 4-digit year")
            except ValueError:
                errors.append("Publication year must be a valid number")

        valid_formats = ["hardcover", "paperback", "ebook", "audiobook"]
        if format and format.lower() not in valid_formats:
            errors.append(f"Format must be one of: {', '.join(valid_formats)}")

        valid_statuses = ["available", "borrowed", "reserved", "unavailable", "maintenance"]
        if format and format.lower() not in valid_formats:
            errors.append(f"Format must be one of: {', '.join(valid_formats)}")

        return errors

    def add_book(self, title, author_id=None, genre=None, publication_year=None,
                format=None, availability_status="available"):
        validation_errors = self.validate_book_data(title, author_id, genre, publication_year, format)

        if validation_errors:
            return False, validation_errors

        success, result = self.book_repository.add_book(
            title, author_id, genre, publication_year, format, availability_status
        )

        if success:
            book_id = result
            logging.info(f"Book '{title}' added successfully with ID {book_id}")
            return True, f"Book added successfully with ID {book_id}"
        else:
            logging.error(f"Book addition failed: {result}")
            return False, [result]

    def get_book(self, book_id):
        result = self.book_repository.get_book(book_id)

        if not result:
            return None

        book = Book(
            book_id=result['book_id'],
            title=result['title'],
            author_id=result['author_id'],
            author_name=result.get('author_name'),
            genre=result['genre'],
            publication_year=result['publication_year'],
            format=result['format'],
            availability_status=result['availability_status']
        )

        return book

    def update_book(self, book_id, title=None, author_id=None, genre=None,
                   publication_year=None, format=None):
        validation_errors = self.validate_book_data(
            title if title is not None else "Book Title",
            author_id, genre, publication_year, format
        )

        if validation_errors:
            return False, validation_errors

        success, message = self.book_repository.update_book(
            book_id, title, author_id, genre, publication_year, format
        )

        if success:
            logging.info(f"Book {book_id} updated successfully")
            return True, "Book updated successfully"
        else:
            logging.error(f"Book update failed: {message}")
            return False, [message]

    def delete_book(self, book_id):
        success, message = self.book_repository.delete_book(book_id)

        if success:
            logging.info(f"Book {book_id} deleted")
            return True, message
        else:
            logging.error(f"Book deletion failed: {message}")
            return False, [message]

    def search_books(self, title=None, author=None, genre=None):
        results = self.book_repository.search_books(title, author, genre)

        books = []
        for book_data in results:
            book = Book(
                book_id=book_data['book_id'],
                title=book_data['title'],
                author_id=book_data['author_id'],
                author_name=book_data.get('author_name'),
                genre=book_data['genre'],
                publication_year=book_data['publication_year'],
                format=book_data['format'],
                availability_status=book_data['availability_status']
            )
            books.append(book)

        return books

    def update_book_status(self, book_id, status):
        valid_statuses = ["available", "borrowed", "reserved", "unavailable", "maintenance"]
        if status not in valid_statuses:
            return False, [f"Invalid status. Must be one of: {', '.join(valid_statuses)}"]

        success, message = self.book_repository.update_book_status(book_id, status)

        if success:
            logging.info(f"Book {book_id} status updated to {status}")
            return True, "Book status updated successfully"
        else:
            logging.error(f"Book status update failed: {message}")
            return False, [message]

    def get_available_books(self):
        results = self.book_repository.get_available_books()

        books = []
        for book_data in results:
            book = Book(
                book_id=book_data['book_id'],
                title=book_data['title'],
                author_id=book_data['author_id'],
                author_name=book_data.get('author_name'),
                genre=book_data['genre'],
                publication_year=book_data['publication_year'],
                format=book_data['format'],
                availability_status=book_data['availability_status']
            )
            books.append(book)

        return books
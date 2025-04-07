from app.models import Author
from repositories.author_repository import AuthorRepository
import logging
import re

class AuthorController:
    def __init__(self):
        self.author_repository = AuthorRepository()
        logging.info("Author controller initialized")

    def validate_author_data(self, name, bio=None):
        errors = []

        if not name or not re.match(r'^[a-zA-Z\s\-\.,]{2,100}$', name):
            errors.append("Author name must be 2-100 characters and contain only letters, spaces, hyphens, periods, and commas")

        if bio and len(bio) > 5000:
            errors.append("Author bio is too long (maximum 5000 characters)")

        return errors

    def add_author(self, name, bio=None):
        validation_errors = self.validate_author_data(name, bio)

        if validation_errors:
            return False, validation_errors

        success, result = self.author_repository.add_author(name, bio)

        if success:
            author_id = result
            logging.info(f"Author '{name}' added successfully with ID {author_id}")
            return True, f"Author added successfully with ID {author_id}"
        else:
            logging.error(f"Author addition failed: {result}")
            return False, [result]

    def get_author(self, author_id):
        result = self.author_repository.get_author(author_id)

        if not result:
            return None

        author = Author(
            author_id=result['author_id'],
            name=result['name'],
            bio=result['bio']
        )

        return author

    def update_author(self, author_id, name=None, bio=None):
        if name is not None or bio is not None:
            validation_errors = self.validate_author_data(
                name if name is not None else "Author Name",
                bio
            )

            if validation_errors:
                return False, validation_errors

        success, message = self.author_repository.update_author(author_id, name, bio)

        if success:
            logging.info(f"Author {author_id} updated successfully")
            return True, "Author updated successfully"
        else:
            logging.error(f"Author update failed: {message}")
            return False, [message]

    def delete_author(self, author_id):
        success, message = self.author_repository.delete_author(author_id)

        if success:
            logging.info(f"Author {author_id} deleted")
            return True, message
        else:
            logging.error(f"Author deletion failed: {message}")
            return False, [message]

    def search_authors(self, search_term=None):
        results = self.author_repository.search_authors(search_term)

        authors = []
        for author_data in results:
            author = Author(
                author_id=author_data['author_id'],
                name=author_data['name'],
                bio=author_data['bio']
            )
            authors.append(author)

        return authors

    def get_author_books(self, author_id):
        results = self.author_repository.get_author_books(author_id)

        if not results:
            author = self.get_author(author_id)
            if not author:
                return False, "Author not found"
            return True, []

        return True, results
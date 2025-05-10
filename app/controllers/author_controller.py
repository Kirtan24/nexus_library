from app.repositories.author_repository import AuthorRepository
import logging

class AuthorController:
    def __init__(self):
        self.author_repository = AuthorRepository()
        logging.info("Author controller initialized")

    def validate_author_data(self, name):
        errors = []
        if not name or len(name) < 2 or len(name) > 100:
            errors.append("Author name must be between 2 and 100 characters")
        return errors

    def add_author(self, name, bio=None, nationality=None, genres=None):
        validation_errors = self.validate_author_data(name)

        if validation_errors:
            return False, validation_errors

        success, result = self.author_repository.add_author(
            name, bio, nationality, genres
        )

        if success:
            logging.info(f"Author '{name}' added successfully with ID {result}")
            return True, f"Author added successfully with ID {result}"
        else:
            logging.error(f"Author addition failed: {result}")
            return False, [result]

    def get_author(self, author_id):
        result = self.author_repository.get_author(author_id)
        return result if result else None

    def update_author(self, author_id, name=None, bio=None, nationality=None, genres=None):
        if name:
            current_author = self.get_author(author_id)
            if not current_author:
                return False, ["Author not found"]

            validation_errors = self.validate_author_data(name)
            if validation_errors:
                return False, validation_errors

        success, message = self.author_repository.update_author(
            author_id, name, bio, nationality, genres
        )

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

    def search_authors(self, name=None, nationality=None):
        return self.author_repository.search_authors(name, nationality)

    def get_all_authors(self):
        return self.author_repository.get_all_authors()

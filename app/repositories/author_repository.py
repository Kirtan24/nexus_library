from app.models import Author
from controllers.db_controller import DatabaseController
import logging

class AuthorRepository:
    def __init__(self):
        self.db_controller = DatabaseController()
        logging.info("AuthorRepository initialized")

    def add_author(self, name, bio=None):
        try:
            query = """
                INSERT INTO authors (name, bio)
                VALUES (%s, %s)
                RETURNING author_id;
            """
            result = self.db_controller.execute_query(query, (name, bio), True)

            if not result:
                return False, "Failed to add author"

            author_id = result[0]['author_id']
            logging.info(f"Author '{name}' added with ID {author_id}")
            return True, author_id

        except Exception as e:
            logging.error(f"Failed to add author: {e}")
            return False, str(e)

    def get_author(self, author_id):
        try:
            query = "SELECT * FROM authors WHERE author_id = %s;"
            result = self.db_controller.execute_query(query, (author_id,), True)

            if not result:
                return None

            return result[0]

        except Exception as e:
            logging.error(f"Failed to retrieve author: {e}")
            return None

    def update_author(self, author_id, name=None, bio=None):
        try:
            update_parts = []
            params = []

            if name is not None:
                update_parts.append("name = %s")
                params.append(name)

            if bio is not None:
                update_parts.append("bio = %s")
                params.append(bio)

            if not update_parts:
                return True, "No updates provided"

            query = f"""
                UPDATE authors
                SET {', '.join(update_parts)}
                WHERE author_id = %s
                RETURNING author_id;
            """
            params.append(author_id)

            result = self.db_controller.execute_query(query, tuple(params), True)

            if not result:
                return False, "Author not found"

            logging.info(f"Author {author_id} updated")
            return True, "Author updated successfully"

        except Exception as e:
            logging.error(f"Failed to update author: {e}")
            return False, str(e)

    def delete_author(self, author_id):
        try:
            check_query = "SELECT COUNT(*) as count FROM books WHERE author_id = %s;"
            check_result = self.db_controller.execute_query(check_query, (author_id,), True)

            has_books = check_result[0]['count'] > 0

            delete_query = "DELETE FROM authors WHERE author_id = %s RETURNING author_id;"
            result = self.db_controller.execute_query(delete_query, (author_id,), True)

            if not result:
                return False, "Author not found"

            if has_books:
                logging.info(f"Author {author_id} deleted, their books now have no author")
                return True, "Author deleted. Note: Books by this author now have no author assigned."
            else:
                logging.info(f"Author {author_id} deleted (had no books)")
                return True, "Author deleted successfully"

        except Exception as e:
            logging.error(f"Failed to delete author: {e}")
            return False, str(e)

    def search_authors(self, search_term=None):
        try:
            if search_term:
                query = "SELECT * FROM authors WHERE name ILIKE %s ORDER BY name ASC;"
                results = self.db_controller.execute_query(query, (f"%{search_term}%",), True)
            else:
                query = "SELECT * FROM authors ORDER BY name ASC;"
                results = self.db_controller.execute_query(query, None, True)

            return results

        except Exception as e:
            logging.error(f"Author search failed: {e}")
            return []

    def get_author_books(self, author_id):
        try:
            query = """
                SELECT book_id, title, genre, publication_year, format, availability_status
                FROM books
                WHERE author_id = %s
                ORDER BY title ASC;
            """
            results = self.db_controller.execute_query(query, (author_id,), True)
            return results

        except Exception as e:
            logging.error(f"Failed to retrieve author's books: {e}")
            return []
import logging
from app.controllers.db_controller import DatabaseController

class AuthorRepository:
    def __init__(self):
        self.db = DatabaseController()
        logging.info("AuthorRepository initialized")

    def add_author(self, name, bio=None, nationality=None, genres=None):

        try:
            query = """
                INSERT INTO authors (name, bio, nationality, genres)
                VALUES (%s, %s, %s, %s)
                RETURNING author_id;
            """
            result = self.db.execute_query(query, (name, bio, nationality, genres), True)

            if not result:
                return False, "Failed to add author"

            if isinstance(result, list) and len(result) > 0:
                author_id = result[0]['author_id']
            elif isinstance(result, dict) and 'author_id' in result:
                author_id = result['author_id']
            else:
                return False, "Failed to get author ID from database"

            logging.info("Author '%s' added with ID %s", name, author_id)
            return True, author_id
        except Exception as e:
            logging.error("Add author error: %s", e)
            return False, str(e)

    def get_author(self, author_id):
        try:
            query = "SELECT * FROM authors WHERE author_id = %s;"
            result = self.db.execute_query(query, (author_id,), True)

            if isinstance(result, list) and len(result) > 0:
                return result[0]
            return result
        except Exception as e:
            logging.error("Get author error: %s", e)
            return None

    def update_author(self, author_id, name=None, bio=None, nationality=None, genres=None):
        try:
            fields = []
            values = []

            if name is not None:
                fields.append("name = %s")
                values.append(name)
            if bio is not None:
                fields.append("bio = %s")
                values.append(bio)
            if nationality is not None:
                fields.append("nationality = %s")
                values.append(nationality)
            if genres is not None:
                fields.append("genres = %s")
                values.append(genres)

            if not fields:
                return True, "No updates provided"

            values.append(author_id)
            query = """
                UPDATE authors
                SET %s
                WHERE author_id = %%s
                RETURNING author_id;
            """ % ", ".join(fields)
            result = self.db.execute_query(query, tuple(values), True)

            if not result:
                return False, "Author not found"

            if isinstance(result, list) and len(result) > 0:
                logging.info("Author %s updated", author_id)
                return True, "Author updated successfully"
            elif isinstance(result, dict) and 'author_id' in result:
                logging.info("Author %s updated", author_id)
                return True, "Author updated successfully"
            else:
                return False, "Failed to update author"

        except Exception as e:
            logging.error("Update author error: %s", e)
            return False, str(e)

    def delete_author(self, author_id):
        try:
            check_query = "SELECT COUNT(*) AS count FROM items WHERE author_id = %s;"
            check_result = self.db.execute_query(check_query, (author_id,), True)

            item_count = 0
            if isinstance(check_result, list) and len(check_result) > 0:
                item_count = check_result[0]['count']
            elif isinstance(check_result, dict) and 'count' in check_result:
                item_count = check_result['count']

            if item_count > 0:
                return False, "Cannot delete author with associated library items"

            delete_query = "DELETE FROM authors WHERE author_id = %s RETURNING author_id;"
            result = self.db.execute_query(delete_query, (author_id,), True)

            if not result:
                return False, "Author not found"

            if (isinstance(result, list) and len(result) > 0) or (isinstance(result, dict) and 'author_id' in result):
                logging.info("Author %s deleted", author_id)
                return True, "Author deleted successfully"
            else:
                return False, "Failed to delete author"

        except Exception as e:
            logging.error("Delete author error: %s", e)
            return False, str(e)

    def search_authors(self, name=None, nationality=None):
        try:
            query = "SELECT * FROM authors WHERE 1=1"
            params = []

            if name:
                query += " AND name ILIKE %s"
                params.append("%" + name + "%")
            if nationality:
                query += " AND nationality ILIKE %s"
                params.append("%" + nationality + "%")

            query += " ORDER BY name ASC"
            result = self.db.execute_query(query, tuple(params), True)

            if result is None:
                return []
            if not isinstance(result, list):
                return [result] if result else []
            return result

        except Exception as e:
            logging.error("Search authors error: %s", e)
            return []

    def get_all_authors(self):
        try:
            query = "SELECT * FROM authors ORDER BY name ASC;"
            result = self.db.execute_query(query, params=(), fetch_results=True)

            logging.debug(f"get_all_authors result type: {type(result)}")
            logging.debug(f"get_all_authors result: {result}")

            if result is None:
                return []
            if not isinstance(result, list):
                return [result] if result else []
            return result

        except Exception as e:
            logging.error("Get all authors error: %s", e)
            return []
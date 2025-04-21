# repositories/book_repository.py
from controllers.db_controller import DatabaseController
import logging

class BookRepository:
    """Repository for managing library items in the database"""

    _instance = None

    # Implementing Singleton pattern
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BookRepository, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized') and self.initialized:
            return

        self.db_controller = DatabaseController()
        self.initialized = True
        logging.info("BookRepository initialized (Singleton)")

    def add_item(self, library_item):
        """
        Add a library item to the database

        Args:
            library_item: Dictionary containing library item details

        Returns:
            Tuple of (success, result) where result is either the new item ID or an error message
        """
        try:
            # First, insert into the main books table
            query = """
                INSERT INTO books (title, author_id, genre, publication_year,
                               availability_status, item_type)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING book_id;
            """
            result = self.db_controller.execute_query(
                query,
                (
                    library_item['title'],
                    library_item['author_id'],
                    library_item.get('genre'),
                    library_item.get('publication_year'),
                    library_item.get('availability_status', 'Available'),
                    library_item['item_type']
                ),
                True
            )

            if not result:
                return False, "Failed to add library item"

            book_id = result[0]['book_id']

            # Now insert into the specific type table based on item_type
            if library_item['item_type'] == 'PrintedBook':
                self._add_printed_book_details(book_id, library_item)
            elif library_item['item_type'] == 'EBook':
                self._add_ebook_details(book_id, library_item)
            elif library_item['item_type'] == 'ResearchPaper':
                self._add_research_paper_details(book_id, library_item)
            elif library_item['item_type'] == 'AudioBook':
                self._add_audiobook_details(book_id, library_item)

            return True, book_id

        except Exception as e:
            logging.error(f"Failed to add library item: {e}")
            return False, str(e)

    def _add_printed_book_details(self, book_id, printed_book):
        """Add details specific to printed books"""
        query = """
            INSERT INTO printed_books (book_id, shelf_location, isbn)
            VALUES (%s, %s, %s);
        """
        self.db_controller.execute_query(
            query,
            (book_id, printed_book.get('shelf_location'), printed_book.get('isbn')),
            False
        )

    def _add_ebook_details(self, book_id, ebook):
        """Add details specific to e-books"""
        query = """
            INSERT INTO ebooks (book_id, file_path, file_size, cover_image_path, description)
            VALUES (%s, %s, %s, %s, %s);
        """
        self.db_controller.execute_query(
            query,
            (book_id, ebook.get('file_path'), ebook.get('file_size'),
             ebook.get('cover_image_path'), ebook.get('description')),
            False
        )

    def _add_research_paper_details(self, book_id, research_paper):
        """Add details specific to research papers"""
        query = """
            INSERT INTO research_papers (book_id, abstract, file_path, journal_name, doi)
            VALUES (%s, %s, %s, %s, %s);
        """
        self.db_controller.execute_query(
            query,
            (book_id, research_paper.get('abstract'), research_paper.get('file_path'),
             research_paper.get('journal_name'), research_paper.get('doi')),
            False
        )

    def _add_audiobook_details(self, book_id, audiobook):
        """Add details specific to audiobooks"""
        query = """
            INSERT INTO audiobooks (book_id, audio_file_path, narrator, duration, description)
            VALUES (%s, %s, %s, %s, %s);
        """
        self.db_controller.execute_query(
            query,
            (book_id, audiobook.get('audio_file_path'), audiobook.get('narrator'),
             audiobook.get('duration'), audiobook.get('description')),
            False
        )

    def get_item(self, book_id):
        """
        Get a library item by ID with all its specific details
        """
        try:
            # First get the basic book info
            query = """
                SELECT b.*, a.name as author_name
                FROM books b
                LEFT JOIN authors a ON b.author_id = a.author_id
                WHERE b.book_id = %s;
            """
            result = self.db_controller.execute_query(query, (book_id,), True)

            if not result:
                return None

            item = result[0]
            item_type = item['item_type']

            # Then get the specific details based on item_type
            if item_type == 'PrintedBook':
                self._get_printed_book_details(book_id, item)
            elif item_type == 'EBook':
                self._get_ebook_details(book_id, item)
            elif item_type == 'ResearchPaper':
                self._get_research_paper_details(book_id, item)
            elif item_type == 'AudioBook':
                self._get_audiobook_details(book_id, item)

            return item

        except Exception as e:
            logging.error(f"Failed to retrieve library item: {e}")
            return None

    def _get_printed_book_details(self, book_id, item_dict):
        """Get printed book specific details"""
        query = "SELECT shelf_location, isbn FROM printed_books WHERE book_id = %s;"
        result = self.db_controller.execute_query(query, (book_id,), True)
        if result:
            item_dict.update(result[0])

    def _get_ebook_details(self, book_id, item_dict):
        """Get e-book specific details"""
        query = """
            SELECT file_path, file_size, cover_image_path, description
            FROM ebooks WHERE book_id = %s;
        """
        result = self.db_controller.execute_query(query, (book_id,), True)
        if result:
            item_dict.update(result[0])

    def _get_research_paper_details(self, book_id, item_dict):
        """Get research paper specific details"""
        query = """
            SELECT abstract, file_path, journal_name, doi
            FROM research_papers WHERE book_id = %s;
        """
        result = self.db_controller.execute_query(query, (book_id,), True)
        if result:
            item_dict.update(result[0])

    def _get_audiobook_details(self, book_id, item_dict):
        """Get audiobook specific details"""
        query = """
            SELECT audio_file_path, narrator, duration, description
            FROM audiobooks WHERE book_id = %s;
        """
        result = self.db_controller.execute_query(query, (book_id,), True)
        if result:
            item_dict.update(result[0])

    def update_item(self, book_id, item_type, **kwargs):
        """Update a library item"""
        try:
            # Update base book details
            base_fields = ['title', 'author_id', 'genre', 'publication_year', 'availability_status']
            update_parts = []
            params = []

            for field in base_fields:
                if field in kwargs and kwargs[field] is not None:
                    update_parts.append(f"{field} = %s")
                    params.append(kwargs[field])

            if update_parts:
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

            # Update type-specific details
            if item_type == 'PrintedBook':
                self._update_printed_book(book_id, kwargs)
            elif item_type == 'EBook':
                self._update_ebook(book_id, kwargs)
            elif item_type == 'ResearchPaper':
                self._update_research_paper(book_id, kwargs)
            elif item_type == 'AudioBook':
                self._update_audiobook(book_id, kwargs)

            return True, "Library item updated successfully"

        except Exception as e:
            logging.error(f"Failed to update library item: {e}")
            return False, str(e)

    def _update_printed_book(self, book_id, fields):
        """Update printed book specific fields"""
        specific_fields = ['shelf_location', 'isbn']
        update_parts = []
        params = []

        for field in specific_fields:
            if field in fields and fields[field] is not None:
                update_parts.append(f"{field} = %s")
                params.append(fields[field])

        if update_parts:
            query = f"""
                UPDATE printed_books
                SET {', '.join(update_parts)}
                WHERE book_id = %s;
            """
            params.append(book_id)
            self.db_controller.execute_query(query, tuple(params), False)

    def _update_ebook(self, book_id, fields):
        """Update e-book specific fields"""
        specific_fields = ['file_path', 'file_size', 'cover_image_path', 'description']
        update_parts = []
        params = []

        for field in specific_fields:
            if field in fields and fields[field] is not None:
                update_parts.append(f"{field} = %s")
                params.append(fields[field])

        if update_parts:
            query = f"""
                UPDATE ebooks
                SET {', '.join(update_parts)}
                WHERE book_id = %s;
            """
            params.append(book_id)
            self.db_controller.execute_query(query, tuple(params), False)

    def _update_research_paper(self, book_id, fields):
        """Update research paper specific fields"""
        specific_fields = ['abstract', 'file_path', 'journal_name', 'doi']
        update_parts = []
        params = []

        for field in specific_fields:
            if field in fields and fields[field] is not None:
                update_parts.append(f"{field} = %s")
                params.append(fields[field])

        if update_parts:
            query = f"""
                UPDATE research_papers
                SET {', '.join(update_parts)}
                WHERE book_id = %s;
            """
            params.append(book_id)
            self.db_controller.execute_query(query, tuple(params), False)

    def _update_audiobook(self, book_id, fields):
        """Update audiobook specific fields"""
        specific_fields = ['audio_file_path', 'narrator', 'duration', 'description']
        update_parts = []
        params = []

        for field in specific_fields:
            if field in fields and fields[field] is not None:
                update_parts.append(f"{field} = %s")
                params.append(fields[field])

        if update_parts:
            query = f"""
                UPDATE audiobooks
                SET {', '.join(update_parts)}
                WHERE book_id = %s;
            """
            params.append(book_id)
            self.db_controller.execute_query(query, tuple(params), False)

    def delete_item(self, book_id):
        """Delete a library item"""
        try:
            # Get item type to know which specific table to delete from
            type_query = "SELECT item_type FROM books WHERE book_id = %s;"
            type_result = self.db_controller.execute_query(type_query, (book_id,), True)

            if not type_result:
                return False, "Library item not found"

            item_type = type_result[0]['item_type']

            # Delete from the specific type table
            specific_table = None
            if item_type == 'PrintedBook':
                specific_table = 'printed_books'
            elif item_type == 'EBook':
                specific_table = 'ebooks'
            elif item_type == 'ResearchPaper':
                specific_table = 'research_papers'
            elif item_type == 'AudioBook':
                specific_table = 'audiobooks'

            if specific_table:
                specific_delete = f"DELETE FROM {specific_table} WHERE book_id = %s;"
                self.db_controller.execute_query(specific_delete, (book_id,), False)

            # Delete from the main books table
            delete_query = "DELETE FROM books WHERE book_id = %s RETURNING book_id;"
            result = self.db_controller.execute_query(delete_query, (book_id,), True)

            return (True, "Library item deleted successfully") if result else (False, "Library item not found")

        except Exception as e:
            logging.error(f"Failed to delete library item: {e}")
            return False, str(e)

    def search_items(self, title=None, author=None, genre=None, item_type=None):
        """Search for library items with various filters"""
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

            if item_type:
                query_parts.append("AND b.item_type = %s")
                params.append(item_type)

            query_parts.append("ORDER BY b.title ASC")
            query = " ".join(query_parts)

            results = self.db_controller.execute_query(query, tuple(params) if params else None, True)

            # For each result, fetch the type-specific details
            for item in results:
                book_id = item['book_id']
                item_type = item['item_type']

                if item_type == 'PrintedBook':
                    self._get_printed_book_details(book_id, item)
                elif item_type == 'EBook':
                    self._get_ebook_details(book_id, item)
                elif item_type == 'ResearchPaper':
                    self._get_research_paper_details(book_id, item)
                elif item_type == 'AudioBook':
                    self._get_audiobook_details(book_id, item)

            return results

        except Exception as e:
            logging.error(f"Library item search failed: {e}")
            return []

    def update_item_status(self, book_id, status):
        """Update a library item's availability status"""
        try:
            query = """
                UPDATE books
                SET availability_status = %s
                WHERE book_id = %s
                RETURNING book_id;
            """
            result = self.db_controller.execute_query(query, (status, book_id), True)
            return (True, "Library item status updated successfully") if result else (False, "Library item not found")

        except Exception as e:
            logging.error(f"Failed to update library item status: {e}")
            return False, str(e)

    def get_available_items(self, item_type=None):
        """Get all available library items, optionally filtered by type"""
        try:
            query_parts = [
                "SELECT b.*, a.name as author_name",
                "FROM books b",
                "LEFT JOIN authors a ON b.author_id = a.author_id",
                "WHERE b.availability_status = 'Available'"
            ]

            params = []

            if item_type:
                query_parts.append("AND b.item_type = %s")
                params.append(item_type)

            query_parts.append("ORDER BY b.title ASC")
            query = " ".join(query_parts)

            results = self.db_controller.execute_query(query, tuple(params) if params else None, True)

            # For each result, fetch the type-specific details
            for item in results:
                book_id = item['book_id']
                item_type = item['item_type']

                if item_type == 'PrintedBook':
                    self._get_printed_book_details(book_id, item)
                elif item_type == 'EBook':
                    self._get_ebook_details(book_id, item)
                elif item_type == 'ResearchPaper':
                    self._get_research_paper_details(book_id, item)
                elif item_type == 'AudioBook':
                    self._get_audiobook_details(book_id, item)

            return results

        except Exception as e:
            logging.error(f"Failed to retrieve available library items: {e}")
            return []
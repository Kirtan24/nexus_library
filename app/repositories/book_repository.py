from app.controllers.db_controller import DatabaseController
from app.services.observer_service import ObserverService

class BookRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BookRepository, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized') and self.initialized:
            return

        self.db_controller = DatabaseController()
        self.observer_service = ObserverService()
        self.initialized = True

    def add_item(self, library_item):
        try:
            check_query = """
                SELECT item_id FROM items
                WHERE title = %s AND author_id = %s AND item_type = %s
            """
            check_params = (
                library_item['title'],
                library_item['author_id'],
                library_item['item_type']
            )

            existing = self.db_controller.execute_query(check_query, check_params, True)
            if existing:
                return False, "Item with same title and author already exists"

            query = """
                INSERT INTO items (title, author_id, genre, publication_year,
                               availability_status, item_type)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING item_id;
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

            item_id = result[0]['item_id']

            if library_item['item_type'] == 'PrintedBook':
                self._add_printed_book_details(item_id, library_item)
            elif library_item['item_type'] == 'EBook':
                self._add_ebook_details(item_id, library_item)
            elif library_item['item_type'] == 'ResearchPaper':
                self._add_research_paper_details(item_id, library_item)
            elif library_item['item_type'] == 'AudioBook':
                self._add_audiobook_details(item_id, library_item)

            return True, item_id

        except Exception as e:
            return False, str(e)

    def _add_printed_book_details(self, item_id, printed_book):
        query = """
            INSERT INTO printed_books (item_id, shelf_location, isbn, total_copies, available_copies)
            VALUES (%s, %s, %s, %s, %s);
        """
        self.db_controller.execute_query(
            query,
            (
                item_id,
                printed_book.get('shelf_location'),
                printed_book.get('isbn'),
                printed_book.get('total_copies', 1),
                printed_book.get('available_copies', 1)
            ),
            False
        )

    def _add_ebook_details(self, item_id, ebook):
        query = """
            INSERT INTO ebooks (item_id, cover_image_url, description)
            VALUES (%s, %s, %s);
        """
        self.db_controller.execute_query(
            query,
            (item_id, ebook.get('cover_image_url'), ebook.get('description')),
            False
        )

    def _add_research_paper_details(self, item_id, research_paper):
        query = """
            INSERT INTO research_papers (item_id, abstract, journal_name, doi)
            VALUES (%s, %s, %s, %s);
        """
        self.db_controller.execute_query(
            query,
            (item_id, research_paper.get('abstract'),
             research_paper.get('journal_name'), research_paper.get('doi')),
            False
        )

    def _add_audiobook_details(self, item_id, audiobook):
        query = """
            INSERT INTO audiobooks (item_id, narrator, duration_minutes, description)
            VALUES (%s, %s, %s, %s);
        """
        self.db_controller.execute_query(
            query,
            (item_id, audiobook.get('narrator'),
             audiobook.get('duration'), audiobook.get('description')),
            False
        )

    def get_item(self, item_id):
        try:
            query = """
                SELECT i.*, a.name as author_name
                FROM items i
                LEFT JOIN authors a ON i.author_id = a.author_id
                WHERE i.item_id = %s;
            """
            result = self.db_controller.execute_query(query, (item_id,), True)

            if not result:
                return None

            item = result[0]
            item_type = item['item_type']

            if item_type == 'PrintedBook':
                self._get_printed_book_details(item_id, item)
            elif item_type == 'EBook':
                self._get_ebook_details(item_id, item)
            elif item_type == 'ResearchPaper':
                self._get_research_paper_details(item_id, item)
            elif item_type == 'AudioBook':
                self._get_audiobook_details(item_id, item)

            return item

        except Exception as e:
            return None

    def _get_printed_book_details(self, item_id, item_dict):
        query = "SELECT shelf_location, isbn, total_copies, available_copies FROM printed_books WHERE item_id = %s;"
        result = self.db_controller.execute_query(query, (item_id,), True)
        if result:
            item_dict.update(result[0])

    def _get_ebook_details(self, item_id, item_dict):
        query = """
            SELECT cover_image_url, description
            FROM ebooks WHERE item_id = %s;
        """
        result = self.db_controller.execute_query(query, (item_id,), True)
        if result:
            item_dict.update(result[0])

    def _get_research_paper_details(self, item_id, item_dict):
        query = """
            SELECT abstract, journal_name, doi
            FROM research_papers WHERE item_id = %s;
        """
        result = self.db_controller.execute_query(query, (item_id,), True)
        if result:
            item_dict.update(result[0])

    def _get_audiobook_details(self, item_id, item_dict):
        query = """
            SELECT narrator, duration_minutes, description
            FROM audiobooks WHERE item_id = %s;
        """
        result = self.db_controller.execute_query(query, (item_id,), True)
        if result:
            item_dict.update(result[0])

    def update_item(self, item_id, item_type, **kwargs):
        try:
            current_status_query = "SELECT availability_status FROM items WHERE item_id = %s;"
            current_status_result = self.db_controller.execute_query(current_status_query, (item_id,), True)
            current_status = current_status_result[0]['availability_status'] if current_status_result else None

            base_fields = ['title', 'author_id', 'genre', 'publication_year', 'availability_status']
            update_parts = []
            params = []

            for field in base_fields:
                if field in kwargs and kwargs[field] is not None:
                    update_parts.append(f"{field} = %s")
                    params.append(kwargs[field])

            if update_parts:
                query = f"""
                    UPDATE items
                    SET {', '.join(update_parts)}
                    WHERE item_id = %s
                    RETURNING item_id;
                """
                params.append(item_id)
                result = self.db_controller.execute_query(query, tuple(params), True)

                if not result:
                    return False, "Item not found"

            if item_type == 'PrintedBook':
                self._update_printed_book(item_id, kwargs)
            elif item_type == 'EBook':
                self._update_ebook(item_id, kwargs)
            elif item_type == 'ResearchPaper':
                self._update_research_paper(item_id, kwargs)
            elif item_type == 'AudioBook':
                self._update_audiobook(item_id, kwargs)

            new_status = kwargs.get('availability_status')
            if (new_status and new_status != current_status and
                new_status.lower() == 'available'):
                self.observer_service.notify(item_id)

            return True, "Library item updated successfully"

        except Exception as e:
            return False, str(e)

    def _update_printed_book(self, item_id, fields):
        specific_fields = ['shelf_location', 'isbn', 'total_copies', 'available_copies']
        self._update_type_table('printed_books', item_id, fields, specific_fields)

    def _update_ebook(self, item_id, fields):
        specific_fields = ['cover_image_url', 'description']
        self._update_type_table('ebooks', item_id, fields, specific_fields)

    def _update_research_paper(self, item_id, fields):
        specific_fields = ['abstract', 'journal_name', 'doi']
        self._update_type_table('research_papers', item_id, fields, specific_fields)

    def _update_audiobook(self, item_id, fields):
        specific_fields = ['narrator', 'duration_minutes', 'description']
        self._update_type_table('audiobooks', item_id, fields, specific_fields)

    def _update_type_table(self, table_name, item_id, fields, specific_fields):
        update_parts = []
        params = []

        for field in specific_fields:
            if field in fields and fields[field] is not None:
                update_parts.append(f"{field} = %s")
                params.append(fields[field])

        if update_parts:
            query = f"""
                UPDATE {table_name}
                SET {', '.join(update_parts)}
                WHERE item_id = %s;
            """
            params.append(item_id)
            self.db_controller.execute_query(query, tuple(params), False)

    def delete_item(self, item_id):
        try:
            type_query = "SELECT item_type FROM items WHERE item_id = %s;"
            type_result = self.db_controller.execute_query(type_query, (item_id,), True)

            if not type_result:
                return False, "Library item not found"

            item_type = type_result[0]['item_type']

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
                specific_delete = f"DELETE FROM {specific_table} WHERE item_id = %s;"
                self.db_controller.execute_query(specific_delete, (item_id,), False)

            delete_query = "DELETE FROM items WHERE item_id = %s RETURNING item_id;"
            result = self.db_controller.execute_query(delete_query, (item_id,), True)

            return (True, "Library item deleted successfully") if result else (False, "Library item not found")

        except Exception as e:
            return False, str(e)

    def search_items(self, title=None, author=None, genre=None, item_type=None, exclude_research_papers=False):
        try:
            query_parts = ["SELECT i.*, a.name as author_name FROM items i LEFT JOIN authors a ON i.author_id = a.author_id WHERE 1=1"]
            params = []

            if title:
                query_parts.append("AND i.title ILIKE %s")
                params.append(f"%{title}%")

            if author:
                query_parts.append("AND a.name ILIKE %s")
                params.append(f"%{author}%")

            if genre:
                query_parts.append("AND i.genre ILIKE %s")
                params.append(f"%{genre}%")

            if item_type:
                query_parts.append("AND i.item_type = %s")
                params.append(item_type)
            elif exclude_research_papers:
                query_parts.append("AND i.item_type != 'ResearchPaper'")

            query_parts.append("ORDER BY i.title ASC")
            query = " ".join(query_parts)

            results = self.db_controller.execute_query(query, tuple(params) if params else None, True)

            for item in results:
                item_id = item['item_id']
                item_type = item['item_type']

                if item_type == 'PrintedBook':
                    self._get_printed_book_details(item_id, item)
                elif item_type == 'EBook':
                    self._get_ebook_details(item_id, item)
                elif item_type == 'AudioBook':
                    self._get_audiobook_details(item_id, item)

            return results

        except Exception as e:
            return []

    def search(self, query, params):
        return self.db_controller.execute_query(query, params, fetch_results=True)

    def update_item_status(self, item_id, status):
        try:
            current_status_query = "SELECT availability_status FROM items WHERE item_id = %s;"
            current_status_result = self.db_controller.execute_query(current_status_query, (item_id,), True)
            current_status = current_status_result[0]['availability_status'] if current_status_result else None

            query = """
                UPDATE items
                SET availability_status = %s
                WHERE item_id = %s
                RETURNING item_id;
            """
            result = self.db_controller.execute_query(query, (status, item_id), True)

            if not result:
                return False, "Library item not found"

            if status.lower() == 'available' and current_status != status:
                self.observer_service.notify(item_id)

            return True, "Library item status updated successfully"

        except Exception as e:
            return False, str(e)

    def get_available_items(self, item_type=None, exclude_research_papers=False):
        try:
            query_parts = [
                "SELECT i.*, a.name as author_name",
                "FROM items i",
                "LEFT JOIN authors a ON i.author_id = a.author_id",
                "WHERE i.availability_status IN ('Available', 'Unavailable')"
            ]

            params = []

            if item_type:
                query_parts.append("AND i.item_type = %s")
                params.append(item_type)
            elif exclude_research_papers:
                query_parts.append("AND i.item_type != 'ResearchPaper'")

            query_parts.append("ORDER BY i.title ASC")
            query = " ".join(query_parts)

            results = self.db_controller.execute_query(query, tuple(params) if params else None, True)

            for item in results:
                item_id = item['item_id']
                item_type = item['item_type']

                if item_type == 'PrintedBook':
                    self._get_printed_book_details(item_id, item)
                elif item_type == 'EBook':
                    self._get_ebook_details(item_id, item)
                elif item_type == 'AudioBook':
                    self._get_audiobook_details(item_id, item)

            return results

        except Exception as e:
            return []

# controllers/library_controller.py
from app.services.book_services import BookService, LibraryItemBuilder

class LibraryController:
    """
    Main controller for library operations.
    Implements Singleton pattern.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LibraryController, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return

        self.book_service = BookService()
        self.initialized = True

    def add_item(self, item_type, title, author_id, **kwargs):
        """
        Add item using Builder pattern for complex construction
        """
        builder = LibraryItemBuilder(item_type, title, author_id)

        # Common attributes
        if 'genre' in kwargs:
            builder.with_genre(kwargs['genre'])
        if 'publication_year' in kwargs:
            builder.with_publication_year(kwargs['publication_year'])
        if 'availability_status' in kwargs:
            builder.with_availability_status(kwargs['availability_status'])

        # Type-specific attributes
        if item_type == 'PrintedBook':
            if 'shelf_location' in kwargs:
                builder.with_shelf_location(kwargs['shelf_location'])
            if 'isbn' in kwargs:
                builder.with_isbn(kwargs['isbn'])

        elif item_type == 'EBook':
            if 'description' in kwargs:
                builder.with_description(kwargs['description'])

        elif item_type == 'ResearchPaper':
            if 'abstract' in kwargs:
                builder.with_abstract(kwargs['abstract'])
            if 'journal_name' in kwargs:
                builder.with_journal_name(kwargs['journal_name'])
            if 'doi' in kwargs:
                builder.with_doi(kwargs['doi'])

        elif item_type == 'AudioBook':
            if 'narrator' in kwargs:
                builder.with_narrator(kwargs['narrator'])
            if 'duration' in kwargs:
                builder.with_duration(kwargs['duration'])
            if 'description' in kwargs:
                builder.with_description(kwargs['description'])

        return builder.add_to_library()

    def get_item(self, book_id):
        """Get item details by ID"""
        return self.book_service.get_item(book_id)

    def search_items(self, title=None, author=None, genre=None, item_type=None):
        """Search items with filters"""
        return self.book_service.search_items(
            title=title,
            author=author,
            genre=genre,
            item_type=item_type
        )

    def update_item(self, book_id, item_type, **kwargs):
        """Update item details"""
        return self.book_service.update_item(book_id, item_type, **kwargs)

    def delete_item(self, book_id):
        """Remove item from library"""
        return self.book_service.delete_item(book_id)

    def update_status(self, book_id, status):
        """Update availability status"""
        return self.book_service.update_item_status(book_id, status)

    def get_available_items(self, item_type=None):
        """Get all available items (optionally filtered by type)"""
        return self.book_service.get_available_items(item_type)
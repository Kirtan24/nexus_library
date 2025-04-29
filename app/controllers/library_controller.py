import logging
from app.services.book_services import BookService, LibraryItemBuilder

class LibraryController:
    """
    Controller class for managing library operations.
    Acts as an interface between the UI/API and the business logic.
    Implements Singleton pattern.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LibraryController, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized') and self.initialized:
            return

        self.book_service = BookService()
        self.initialized = True
        logging.info("LibraryController initialized (Singleton)")

    def add_item(self, **kwargs):
        """
        Add a new library item directly
        """
        return self.book_service.add_item(**kwargs)

    def add_item_with_builder(self, item_type, title, author_id, **kwargs):
        """
        Add a new library item using the Builder pattern for more complex items
        """
        # Start with the required parameters
        builder = LibraryItemBuilder(item_type, title, author_id)

        # Add optional common attributes
        if 'genre' in kwargs:
            builder.with_genre(kwargs['genre'])
        if 'publication_year' in kwargs:
            builder.with_publication_year(kwargs['publication_year'])
        if 'availability_status' in kwargs:
            builder.with_availability_status(kwargs['availability_status'])

        # Add type-specific attributes
        if item_type == 'PrintedBook':
            if 'shelf_location' in kwargs:
                builder.with_shelf_location(kwargs['shelf_location'])
            if 'isbn' in kwargs:
                builder.with_isbn(kwargs['isbn'])

        elif item_type == 'EBook':
            if 'file_path' in kwargs:
                builder.with_file_path(kwargs['file_path'])
            if 'file_size' in kwargs:
                builder.with_file_size(kwargs['file_size'])
            if 'cover_image_path' in kwargs:
                builder.with_cover_image(kwargs['cover_image_path'])
            if 'description' in kwargs:
                builder.with_description(kwargs['description'])

        elif item_type == 'ResearchPaper':
            if 'abstract' in kwargs:
                builder.with_abstract(kwargs['abstract'])
            if 'journal_name' in kwargs:
                builder.with_journal_name(kwargs['journal_name'])
            if 'doi' in kwargs:
                builder.with_doi(kwargs['doi'])
            if 'file_path' in kwargs:
                builder.with_file_path(kwargs['file_path'])

        elif item_type == 'AudioBook':
            if 'audio_file_path' in kwargs:
                builder.with_audio_file_path(kwargs['audio_file_path'])
            if 'narrator' in kwargs:
                builder.with_narrator(kwargs['narrator'])
            if 'duration' in kwargs:
                builder.with_duration(kwargs['duration'])
            if 'description' in kwargs:
                builder.with_description(kwargs['description'])

        # Build and add to the library
        return builder.add_to_library()

    def get_item(self, book_id):
        """Get a library item by ID"""
        return self.book_service.get_item(book_id)

    def update_item(self, book_id, item_type, **kwargs):
        """Update a library item by ID"""
        return self.book_service.update_item(book_id, **kwargs)

    def delete_item(self, book_id):
        """Delete a library item by ID"""
        return self.book_service.delete_item(book_id)

    def search_items(self, **filters):
        """
        Search for library items with various filters
        Filters can include: title, author_id, genre, item_type, etc.
        """
        return self.book_service.search_items(**filters)

    def get_all_items(self, page=1, items_per_page=10):
        """
        Get all library items with pagination
        """
        return self.book_service.get_all_items(page, items_per_page)

    def check_out_item(self, book_id, user_id):
        """
        Check out a library item to a user
        """
        return self.book_service.check_out_item(book_id, user_id)

    def return_item(self, book_id):
        """
        Return a checked out library item
        """
        return self.book_service.return_item(book_id)

    def get_user_checked_out_items(self, user_id):
        """
        Get all items checked out by a specific user
        """
        return self.book_service.get_user_checked_out_items(user_id)

    def get_overdue_items(self):
        """
        Get all items that are currently overdue
        """
        return self.book_service.get_overdue_items()

    def generate_report(self, report_type, start_date=None, end_date=None):
        """
        Generate various library reports
        report_type can be: 'circulation', 'acquisition', 'popular_items', etc.
        """
        return self.book_service.generate_report(report_type, start_date, end_date)